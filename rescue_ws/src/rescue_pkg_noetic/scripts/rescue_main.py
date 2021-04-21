#!/usr/bin/env python

# ROS framework / messages
import rospy
from std_msgs.msg import String
from rescue_pkg_noetic.msg import location_command
from rescue_pkg_noetic.msg import co2

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
    rospy.loginfo('RESCUE: Coordinates received: %3.2f, %3.2f, %3.2f',location_msg.coord1,location_msg.coord2,location_msg.coord3)

    if location_msg.type_flag == 'c':
        pivot_angle, rotate_angle = get_pivot_rotate_angles([location_msg.coord1,location_msg.coord2,location_msg.coord3])

        ext_dist = get_ext_dist(location_msg.coord1,location_msg.coord2,location_msg.coord3)

        print("Calculated pivot angle of",pivot_angle,"deg, rotation angle of",rotate_angle,"deg, and extension distance of",ext_dist,"cm")

        # PRE(pivot_angle,rotate_angle,ext_dist)

    elif location_msg.type_flag == 'a':

        print("Received pivot angle of",location_msg.coord1,"deg, rotation angle of",location_msg.coord2,"deg, and extension distance of",location_msg.coord3,"cm")
        # ext_dist = location_msg.coord3 / 100 # convert to cm
        # PRE(location_msg.coord1,location_msg.coord2,ext_dist)
    else:
        # not a valid flag, handle error





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
    co2_pub = rospy.Publisher('co2_data', co2, queue_size=10)

    param = rospy.get_param('type')
    coord1 = rospy.get_param('coord1')
    coord2 = rospy.get_param('coord2')
    coord3 = rospy.get_param('coord3')


    if param == "a":
        print("Given angle and extension distance input")
        print("Given coordinates:",coord1,"deg,",coord2,"deg,",coord3,"cm")
    elif param =="c":
        print("Given relative inertial coordinate input")
        print("Given coordinates:",coord1,"cm,",coord2,"cm,",coord3,"cm")
    else:
        print("Given invalid type flag")
    
    print("\n")

    co2_msg = co2()
    co2_msg.ppm = 1400
    rospy.loginfo("RESCUE: CO2 data sent: %4.2f ppm",co2_msg.ppm)

    rospy.sleep(2)
    co2_pub.publish(co2_msg)
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
        spin()
    except rospy.ROSInterruptException:
        pass