from adafruit_servokit import ServoKit
import adafruit_motor.servo
from dual_g2_hpmd_rpi import motors, MAX_SPEED
import busio
import pwmio
import math
import sys

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
########################################################################
# CONFIGURATION:
# Channel 1: (farthest to the left if power supply inputs are on top)
# Channel 2: (to the right of channel 1)
########################################################################
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

# Temp xyz point:
xyz = [1,1,1]
pivot_angle, rotation_angle = get_pivot_rotate_angles(xyz)
# print("Pivot angle is: ", pivot_angle)
# print("Rotation angle is: ", rotation_angle)
# Command pivot to the required angle
# Command rotation to the required angle
#pivot_rotate_kit.servo[0].angle = pivot_angle*4 # degrees
#pivot_rotate_kit.servo[1].angle = rotation_angle # degrees
pivot_rotate_kit.servo[0].angle = int(sys.argv[1]) # degrees
pivot_rotate_kit.servo[1].angle = int(sys.argv[2]) # degrees
print("Pivot: ",int(sys.argv[1]),"deg")
print("Rotate: ",int(sys.argv[2]),"deg")
motors.enable()
motors.setSpeeds(200,200)

