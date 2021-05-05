#!/usr/bin/env python

# ROS framework / messages
import rospy
from std_msgs.msg import String
from rescue_pkg_noetic.msg import location_command
from rescue_pkg_noetic.msg import co2
from rescue_pkg_noetic.msg import pan_tilt
from rescue_pkg_noetic.msg import sensor_cmd
from rescue_pkg_noetic.msg import video


# PRE
from adafruit_servokit import ServoKit
import adafruit_motor.servo
from dual_g2_hpmd_rpi import motors, MAX_SPEED
import busio
from smc import SMC
import time
import pwmio

# video data
import cv2
from threading import Lock
import os
import re

# general/misc
import math
import numpy as np

# publishers
pan_tilt_pub = rospy.Publisher('pan_tilt_command', pan_tilt, queue_size=10)
sensor_pub = rospy.Publisher('sensor_command', sensor_cmd, queue_size=10)
video_pub = rospy.Publisher('video_data', video, queue_size=10)
status_pub = rospy.Publisher('rescue_status', String, queue_size=10)

# camera name
DEFAULT_CAMERA_NAME = '/dev/v4l/by-id/usb-MACROSIL_AV_TO_USB2.0-video-index0'

class VideoRecorder:
    def __init__(self, cap, path_prefix):
        self.out_filename = None
        self.lock = Lock()
        self.is_recording = False

        self.out = None
        self.cap = cap
        self.record_start_time = time.time()
        self.record_time_limit = 0
        self.path_prefix = path_prefix

    def stop_current_recording(self):
        if self.out is not None:
            self.out.release()
        if self.is_recording:
            print("Stopping recording")
            self.is_recording = False

    def start_new_recording(self, filename):
        fourcc_code = None
        if filename[-4:] == ".mp4":
            fourcc_code = cv2.VideoWriter_fourcc(*"mp4v") #Previously used hardcoded fourcc_code = 0x00000021
        elif filename[-4:] == ".avi":
            fourcc_code = int(cap.get(cv2.CAP_PROP_FOURCC))
        else:
            print("Invalid file type")
            
            return False


        frame_dims = (int(self.cap.get(3)), int(self.cap.get(4)))

        if(not filename.startswith('/')):
            filename = self.path_prefix + filename

        rospy.loginfo("Starting recording for " + filename)
        if(not os.path.exists(os.path.dirname(filename))):
            print("Path does not exist")
            return False

        self.is_recording = True
        self.record_start_time = time.time()

        self.out = cv2.VideoWriter(filename,
                                   fourcc_code,
                                   24,
                                   frame_dims)
        return True

    def save_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Capture Failed")
            self.stop_current_recording()
            return
        self.out.write(frame)

    def check_timeout(self):
        if time.time() - self.record_start_time > self.record_time_limit:
            self.stop_current_recording()
            return False
        return True


    def work_in_loop(self):
        with self.lock:
            if self.is_recording and self.check_timeout():
                self.save_frame()
                return

    def on_close(self):
        with self.lock:
            self.stop_current_recording()



def loc_callback(location_msg):

    # rospy.loginfo('RESCUE: Coordinates received: %3.2f, %3.2f, %3.2f',location_msg.coord1,location_msg.coord2,location_msg.coord3)

    if location_msg.type_flag == 'c':
        rospy.loginfo("RESCUE: Given relative inertial coordinate input")
        pivot_angle, rotate_angle = get_pivot_rotate_angles([location_msg.coord1,location_msg.coord2,location_msg.coord3])

        ext_dist = get_ext_dist(location_msg.coord1,location_msg.coord2,location_msg.coord3)

        rospy.loginfo("RESCUE: Calculated pivot angle of %3.f deg, rotation angle of %3.f deg, and extension distance of %3.1f cm",pivot_angle,rotate_angle,ext_dist)

        ext_time = PRE(pivot_angle,rotate_angle,ext_dist)

    elif location_msg.type_flag == 'a':

        rospy.loginfo("RESCUE: Given relative angle and extension distance input")
        rospy.loginfo("RESCUE: Received pivot angle of %3.f deg, rotation angle of %3.f deg, and extension distance of %3.1f cm",location_msg.coord1,location_msg.coord2,location_msg.coord3)
        # ext_dist = location_msg.coord3 / 100 # convert to cm
        # ext_time = PRE(location_msg.coord1,location_msg.coord2,location_msg.coord3)
    else:
        # not a valid flag, handle error
        rospy.loginfo("RESCUE: Type flag was invalid") 

    # Pan/tilt command
    pan_angle, tilt_angle = pan_tilt_handler()
    rospy.loginfo("RESCUE: Sent pan angle of %3.f deg and tilt angle of %3.f deg",pan_angle,tilt_angle)

    # sensor command
    ext_time = 10
    sensing_time = sensor_cmd_handler(20,ext_time)
    rospy.loginfo("RESCUE: Sent sensing command of duration %3.f seconds", sensing_time)

    video_msg = video()
    video_msg.msg = "Too bad this isn't a video"
    video_pub.publish(video_msg)
    
    # publish after short delay to ensure EE node is active
    # rospy.sleep(1)
    # # co2_pub.publish(co2_msg)
    # pan_tilt_pub.publish(pan_tilt_msg)




def pan_tilt_handler(pan_angle=45,tilt_angle=60):

    pan_tilt_msg = pan_tilt()
    pan_tilt_msg.pan_angle = pan_angle
    pan_tilt_msg.tilt_angle = tilt_angle

    # rospy.sleep(.5)
    pan_tilt_pub.publish(pan_tilt_msg)
    
    return pan_angle, tilt_angle



def sensor_cmd_handler(sensing_time,ext_time):

    # sensor_pub = rospy.Publisher('sensor_command', sensor_cmd, queue_size=10)

    sensor_msg = sensor_cmd()
    sensor_msg.sensing_time = sensing_time
    sensor_msg.ext_time = ext_time

    rospy.sleep(.5)
    sensor_pub.publish(sensor_msg)

    return sensing_time




def get_pivot_rotate_angles(xyz_end):
    '''
    :param xyz_end: list of three points ie [x, y, z]
    :return: two angles (pivot and rotation) in degrees
    '''
    # The step for this is to get a position vector from the base to the endpoint
    # Then project that position vector onto the xy plane and get the angle between the x axis
    # the projected point. This is the rotation angle
    # Repeat the projection onto the x-z axis and get the angle between the x axis and the projected point.

    pivot_angle = math.acos(xyz_end[0]/math.sqrt(xyz_end[0]**2 + xyz_end[1]**2)) * (180/math.pi)
    rotation_angle = math.acos(xyz_end[0]/math.sqrt(xyz_end[0]**2 + xyz_end[2]**2)) * (180/math.pi)
    return pivot_angle, rotation_angle



def get_ext_dist(x,y,z):
    # print('Need to calculate extension distance for x=',x,', y=',y,', z=',z)

    stowed_length = 15.5 / .393701 # [cm] length of arm in stowed position conv. from [in]

    dist = math.sqrt(x**2 + y**2 + z**2) - stowed_length

    return dist

########################################################################
# CONFIGURATION:
# Channel 1: (farthest to the left if power supply inputs are on top)
# Channel 2: (to the right of channel 1)
########################################################################
def PRE(pivot_angle, rotate_angle, extend_length):
    mc = SMC('/dev/ttyACM0', 115200)
    mc.init()
    pivot_rotate_kit = ServoKit(channels=16)
    # The pivot servo should be connected to channel 1
    # pivot_servo = adafruit_motor.servo.Servo(0)
    # The rotation servo should be connected to channel 2
    # rotation_servo = pivot_rotate_kit.servo.Servo(1)
    # 
    # # Set the actuation range, min_pulse, and max_pulse of the pivot servo
    pivot_rotate_kit.servo[0].actuation_range = 600 # degrees
    pivot_rotate_kit.servo[0].min_pulse = (1000)
    pivot_rotate_kit.servo[0].max_pulse = (2000)
    # Set the actuation range, min_pulse, and max_pulse of the rotation servo
    pivot_rotate_kit.servo[1].actuation_range = 600 # degrees
    pivot_rotate_kit.servo[1].min_pulse = (1000)
    pivot_rotate_kit.servo[1].max_pulse = (2000)
    # Command pivot to the required angle
    # Command rotation to the required angle
    pivot_rotate_kit.servo[0].angle = pivot_angle*4 # degrees
    pivot_rotate_kit.servo[1].angle = rotate_angle # degrees


    #########################TEST EXTENSION############################
    # Extension line equation: y = 10x + 20
    time_on = (extend_length - 20)/10
    current_time = time.time()
    
    while time.time() - current_time < time_on:
        mc.speed(-1100)
        
    mc.stop()
    
    time.sleep(30)

    status_pub.publish("Retracting arm, data transmission incoming")
    
    current_time = time.time()
    mc.init()
    while time.time() - current_time < time_on:
        mc.speed(1100)
        
    mc.stop()

    return time_on


def video_record(record_time):
    device_num = 0  #0 captures from webcam (specifically /dev/video0)
    if os.path.exists(DEFAULT_CAMERA_NAME):
        device_path = os.path.realpath(DEFAULT_CAMERA_NAME)
        device_re = re.compile("\/dev\/video(\d+)")
        info = device_re.match(device_path)
        if info:
            device_num = int(info.group(1))

    cap = cv2.VideoCapture(device_num)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 5000)  #Sets the camera to the maximal resolution
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 5000)  # up to 5000 x 5000
    vr = VideoRecorder(cap, "/home/pi/Desktop/")
    vr.start_new_recording("recording.mp4")
    current_time = time.time()
    while time.time() - current_time <= 35:
        vr.save_frame()
        
    vr.on_close()
    cap.release()


def init():
    rospy.init_node('RESCUE_main')#, anonymous=True)

    rospy.Subscriber('location_command', location_command, loc_callback)


def spin():
    
    rospy.sleep(1)
    rospy.spin()
    # rate = rospy.Rate(2) # hz

    # while not rospy.is_shutdown():
    #     co2_msg = co2()
    #     co2_msg.ppm = 1400
    #     rospy.loginfo("CO2 data sent: %4.2f ppm",co2_msg.ppm)

    #     co2_pub.publish(co2_msg)
    #     rate.sleep()



if __name__ == '__main__':
    try:
        init()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
