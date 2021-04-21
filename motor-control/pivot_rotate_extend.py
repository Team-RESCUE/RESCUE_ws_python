from adafruit_servokit import ServoKit
import adafruit_motor.servo
from dual_g2_hpmd_rpi import motors, MAX_SPEED
import busio
from smc import SMC
import time
import pwmio
import math

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
    
    # pivot_rotate_kit.servo[0].angle = 120 # degrees
    # pivot_rotate_kit.servo[1].angle = 395 # degrees
    

PRE(45,315,100)
