#!/usr/bin/env python

# ROS framework / messages
import rospy
from std_msgs.msg import String
from rescue_pkg_noetic.msg import pan_tilt
from rescue_pkg_noetic.msg import sensor_cmd
from rescue_pkg_noetic.msg import co2

import pigpio # GPIO servo control

# CO2 and LED interfacing
from brightpi import *
from scd30_i2c import SCD30
import adafruit_bno055
import busio


# general/misc
import time
import numpy as np
import sys

# Global variables

co2_pub = rospy.Publisher('co2_data', co2, queue_size=10)

# starting angle/pulsewidth values for pan/tilt servos
this_pan_angle = 0
this_tilt_angle = 0
this_pan_pw = 1600
this_tilt_pw = 1000

def sensor_callback(sensor_cmd):
	rospy.loginfo("RESCUE-EE: Sensor call received for %3.f seconds",sensor_cmd.sensing_time)

	co2_msg = co2()
	co2_msg.ppm = 1400 #co2_lights(sensor_cmd.sensing_time)
    
	co2_pub.publish(co2_msg)

	rospy.loginfo("RESCUE-EE: CO2 data sent: %4.2f ppm",co2_msg.ppm)



def pan_tilt_callback(pan_tilt_msg):

	global this_pan_angle, this_tilt_angle, this_pan_pw, this_tilt_pw # to use later	

	pan_angle = pan_tilt_msg.pan_angle
	tilt_angle = pan_tilt_msg.tilt_angle

	rospy.loginfo("RESCUE-EE: Received pan/tilt command: pan %3.f deg, tilt %3.f deg",pan_angle,tilt_angle)

	pan_pw = get_pan_pw(this_pan_angle,pan_angle,this_pan_pw)
	tilt_pw = get_tilt_pw(this_tilt_angle,tilt_angle,this_tilt_pw)

	rospy.loginfo("RESCUE-EE: Corresponding pan/tilt pulsewidths are %5.f and %5.f microseconds, respectively",this_pan_pw,this_tilt_pw)

	pan_pin = 13
	tilt_pin = 12
	# pan_tilt_loop(pan_pw,tilt_pw,pan_pin,tilt_pin)
	pan_loop(pan_pw,pan_pin)

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


def pan_loop(pan_pw,pan_pin):
	global this_pan_pw

	pi = pigpio.pi()

	this_pw = this_pan_pw

	pi.set_mode(pan_pin,pigpio.OUTPUT)
	pi.set_servo_pulsewidth(pan_pin,pan_pw)

	pw_diff = np.absolute(pan_pw-this_pw)
	direction = (pan_pw-this_pw)/pw_diff

	while pw_diff > 20:
		pi.set_servo_pulsewidth(pan_pin,this_pw+direction*pw_diff/2)
		this_pw = pi.get_servo_pulsewidth(pan_pin)
		pw_diff = np.absolute(pan_pw-this_pw)

	pi.set_servo_pulsewidth(pan_pin,pan_pw)

	this_pan_pw = this_pw


def pan_tilt_loop(pan_pw,tilt_pw,pan_pin,tilt_pin):

	global this_pan_pw, this_tilt_pw # to use later	

	pi = pigpio.pi()
	# pins_out = [pan_pin,tilt_pin]
	pins_out = [pan_pin]

	target_pws = [pan_pw,tilt_pw]
	this_pws = [this_pan_pw,this_tilt_pw]
	# pw_diffs = [np.absolute(this_pan_pw-pan_pw),np.absolute(this_tilt_pw-tilt_pw)]
	# directions = [(pan_pw-this_pan_pw)/pw_diffs[0],(tilt_pw-this_tilt_pw)/pw_diffs[1]]

	for i in range(len(pins_out)):
		pi.set_mode(pins_out[i],pigpio.OUTPUT)
		pi.set_servo_pulsewidth(pins_out[i],target_pws[i])

		pw_diff = np.absolute(target_pws[i]-this_pws[i])
		direction = (target_pws[i]-this_pws[i])/pw_diff

		while pw_diff > 20:
			pi.set_servo_pulsewidth(pins_out[i],this_pws[i]+direction*pw_diff/2)
			this_pws[i] = pi.get_servo_pulsewidth(pins_out[i])
			# this_pws[i] = this_pws[i] + direction*pw_diff/2
			# print(this_pws[i])

			pw_diff = np.absolute(this_pws[i]-target_pws[i])
    
		pi.set_servo_pulsewidth(pins_out[i],target_pws[i])

	this_pan_pw = this_pws[0]
	this_tilt_pw = this_pws[1]

	# return 1


def co2_lights(time_on):
    ########################### LED BEGIN ########################################
    # We will need to adjust time_on based on how long the pan/tilt routine takes
    brightPi = BrightPi()
    # Reset the brightpi to ensure it's in its original state
    brightPi.reset()
    # Create an array for the LEDS - lets start with 6
    leds = [1,4]
    
    ########################### AHRS BEGIN #########################################
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bno055.BNO055_I2C(i2c)
    ahrs = []
  
    ########################### CO2 BEGIN ##########################################
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
        ahrs.append(sensor.euler)
        sleep(1)
        if scd30.get_data_ready():
            m = scd30.read_measurement()
            co2.append(m[0])
            
            if m is not None:
                next_time = time.time()
                time.sleep(2)
            else:
                 time.sleep(0.2)
            
            if (next_time - current_time) >= time_on:
                break
                 
    scd30.stop_periodic_measurement()
    brightPi.set_led_on_off(leds, OFF)
    return co2, ahrs


def init():
	rospy.init_node('RESCUE_EE')

	rospy.Subscriber('sensor_command', sensor_cmd, sensor_callback)

	rospy.Subscriber('pan_tilt_command', pan_tilt, pan_tilt_callback)

	rospy.spin()

# def spin():
# 	rospy.spin()


if __name__ == '__main__':
	try:
		init()
		# rospy.spin()
	except rospy.ROSInterruptException:
		pass