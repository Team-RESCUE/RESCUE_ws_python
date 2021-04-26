#!/usr/bin/env python

# ROS framework / messages
import rospy
from std_msgs.msg import String
from rescue_pkg_noetic.msg import location_command
from rescue_pkg_noetic.msg import co2
from rescue_pkg_noetic.msg import pan_tilt


# PRE
# from adafruit_servokit import ServoKit
# import adafruit_motor.servo
# from dual_g2_hpmd_rpi import motors, MAX_SPEED
# import busio
# from smc import SMC
# import time
# import pwmio

# general/misc
import math
import numpy as np


def loc_callback(location_msg):

    # rospy.loginfo('RESCUE: Coordinates received: %3.2f, %3.2f, %3.2f',location_msg.coord1,location_msg.coord2,location_msg.coord3)

    if location_msg.type_flag == 'c':
        rospy.loginfo("RESCUE: Given relative inertial coordinate input")
        pivot_angle, rotate_angle = get_pivot_rotate_angles([location_msg.coord1,location_msg.coord2,location_msg.coord3])

        ext_dist = get_ext_dist(location_msg.coord1,location_msg.coord2,location_msg.coord3)

        rospy.loginfo("RESCUE: Calculated pivot angle of %3.f deg, rotation angle of %3.f deg, and extension distance of %3.1f cm",pivot_angle,rotate_angle,ext_dist)

        # PRE(pivot_angle,rotate_angle,ext_dist)

    elif location_msg.type_flag == 'a':

        rospy.loginfo("RESCUE: Given relative angle and extension distance input")
        rospy.loginfo("RESCUE: Received pivot angle of %3.f deg, rotation angle of %3.f deg, and extension distance of %3.1f cm",location_msg.coord1,location_msg.coord2,location_msg.coord3)
        # ext_dist = location_msg.coord3 / 100 # convert to cm
        # PRE(location_msg.coord1,location_msg.coord2,ext_dist)
    else:
        # not a valid flag, handle error
        rospy.loginfo("RESCUE: Type flag was invalid")



    # CO2 data    
    CO2_handler()
    

    # Pan/tilt command
    pan_tilt_handler()
    
    # publish after short delay to ensure EE node is active
    # rospy.sleep(1)
    # # co2_pub.publish(co2_msg)
    # pan_tilt_pub.publish(pan_tilt_msg)




def CO2_handler(ppm=1):

    co2_pub = rospy.Publisher('co2_data', co2, queue_size=10)

    co2_msg = co2()
    co2_msg.ppm = 1400
    
    co2_pub.publish(co2_msg)

    rospy.loginfo("RESCUE: CO2 data sent: %4.2f ppm",co2_msg.ppm)

    

    return 1


def pan_tilt_handler(pan_angle=45,tilt_angle=60):

    pan_tilt_pub = rospy.Publisher('pan_tilt_command', pan_tilt, queue_size=10)

    pan_tilt_msg = pan_tilt()
    pan_tilt_msg.pan_angle = pan_angle
    pan_tilt_msg.tilt_angle = tilt_angle

    # delay before publishing to ensure EE node is active
    rospy.sleep(1)
    pan_tilt_pub.publish(pan_tilt_msg)

    rospy.loginfo("RESCUE: Sent pan angle of %3.f deg and tilt angle of %3.f deg",pan_tilt_msg.pan_angle,pan_tilt_msg.tilt_angle)

    return 1



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
    print('Need to calculate extension distance for x=',x,', y=',y,', z=',z)

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
    
    current_time = time.time()
    mc.init()
    while time.time() - current_time < time_on:
        mc.speed(1100)
        
    mc.stop()



def init():
    rospy.init_node('RESCUE_main')#, anonymous=True)

    rospy.Subscriber('location_command', location_command, loc_callback)


# def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    # rospy.init_node('RESCUE_main', anonymous=True)

    # rospy.Subscriber('location_command', location_command, callback)

    # spin() simply keeps python from exiting until this node is stopped
    # rospy.spin()



def spin():
    

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