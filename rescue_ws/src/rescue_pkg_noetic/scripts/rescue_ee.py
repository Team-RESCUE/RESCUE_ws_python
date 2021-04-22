#!/usr/bin/env python

# ROS framework / messages
import rospy
from std_msgs.msg import String
from rescue_pkg_noetic.msg import pan_tilt
from rescue_pkg_noetic.msg import sensor_cmd

import pigpio # GPIO servo control

# CO2 and LED interfacing
from brightpi import *
from scd30_i2c import SCD30


# general/misc
import time
import numpy as np
import sys

# Global variables

# starting angle/pulsewidth values for pan/tilt servos
this_pan_angle = 0
this_tilt_angle = 0
this_pan_pw = 1600
this_tilt_pw = 1000

def sensor_callback(sensor_cmd):
	rospy.log("Sensor call received for %3.f seconds",sensor_cmd.sensing_time)
	co2_data = get_co2_data(sensor_cmd.sensing_time)

def pan_tilt_callback(pan_tilt_msg):

	global this_pan_angle, this_tilt_angle, this_pan_pw, this_tilt_pw # to use later	

	pan_angle = pan_tilt_msg.pan_angle
	tilt_angle = pan_tilt_msg.tilt_angle

	rospy.loginfo("RESCUE: Received pan/tilt command: pan",pan_angle,"deg, tilt",tilt_angle,"deg")

	pan_pw = get_pan_pw(this_pan_angle,pan_angle,this_pan_pw)
	tilt_pw = get_tilt_pw(this_tilt_angle,tilt_angle,this_tilt_pw)

	rospy.loginfo("RESCUE: Corresponding pan/tilt pulsewidths are %5.f and %5.f microseconds, respectively",this_pan_pw,this_tilt_pw)

	this_pan_angle = pan_angle
	this_tilt_angle = tilt_angle
	this_pan_pw = pan_pw
	this_tilt_pw = tilt_pw



def get_pan_pw(this_angle,target_angle,this_pw):
	min_angle = 0 #not used, doesn't affect eqn
	max_angle = 90

	# check direction of pan
	direction = (this_angle - target_angle)/np.absolute(this_angle - target_angle)
	pw_limit = 1500 + direction*500 #1000 if panning left, 2000 if right

	target_pw = this_pw + direction * (this_angle-target_angle) * (this_pw-pw_limit) / (max_angle + direction*target_angle)
	
	return target_pw

def get_tilt_pw(this_angle,target_angle,this_pw):
	min_angle = 0 #not used, doesn't affect eqn
	max_angle = 75

	# check direction of pan
	direction = (this_angle - target_angle)/np.absolute(this_angle - target_angle)
	pw_limit = 2000

	target_pw = this_pw + direction * (this_angle-target_angle) * (this_pw-pw_limit) / (max_angle + direction*target_angle)
	
	return target_pw


def get_co2_data(time_on):
    # We will need to adjust time_on based on how long the pan/tilt routine takes
    brightPi = BrightPi()

    # Reset the brightpi to ensure it's in its original state
    brightPi.reset()
    # Create an array for the LEDS - lets start with 6
    leds = [1,4]
    scd30 = SCD30()
    scd30.set_measurement_interval(2)
    
    # Set up the self calibration
    scd30.set_auto_self_calibration(True)
    scd30.start_periodic_measurement()    
    time.sleep(2)
    
    co2 = []
    current_time = time.time()
    brightPi.set_led_on_off(leds, ON)
    while True:
        if scd30.get_data_ready():
            m = scd30.read_measurement()
            co2.append(m[0])
            
            if m is not None:
                # print(f"CO2: {m[0]:.2f}ppm")
                next_time = time.time()
                time.sleep(2)
            else:
                 time.sleep(0.2)
            
            if (next_time - current_time) >= time_on:
                break
                 
    scd30.stop_periodic_measurement()
    brightPi.set_led_on_off(leds, OFF)
    return co2


def init():
	rospy.init_node('RESCUE_EE')

	rospy.Subscriber('sensor_command', sensor_cmd, sensor_callback)

	rospy.Subscriber('pan_tilt_command', pan_tilt, pan_tilt_callback)

# def spin():
# 	rospy.spin()


if __name__ == '__main__':
	try:
		init()
		rospy.spin()
	except rospy.ROSInterruptException:
		pass