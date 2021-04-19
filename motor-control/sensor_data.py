# Import necessary packages
import smbus
import time
import board
import busio
import adafruit_scd30
from scd30_i2c import SCD30
from brightpi import *


def get_co2_data(time_on):
    
    scd30 = SCD30()
    scd30.set_measurement_interval(2)
    
    # Set up the self calibration
    scd30.set_auto_self_calibration(True)
    scd30.start_periodic_measurement()    
    time.sleep(2)
    
    co2 = []
    current_time = time.time()
    
    while True:
        if scd30.get_data_ready():
            m = scd30.read_measurement()
            co2.append(m[0])
            
            if m is not None:
                print(f"CO2: {m[0]:.2f}ppm")
                next_time = time.time()
                time.sleep(2)
            else:
                 time.sleep(0.2)
            
            if (next_time - current_time) >= time_on:
                break
                 
    scd30.stop_periodic_measurement()
    return co2


def activate_led_routine(time_on):
    # We will need to adjust time_on based on how long the pan/tilt routine takes
    brightPi = BrightPi()

    # Reset the brightpi to ensure it's in its original state
    brightPi.reset()
    # Create an array for the LEDS - lets start with 6
    leds = [1,4]
    # Turn them on
    brightPi.set_led_on_off(leds, ON)
    time.sleep(time_on)
    brightPi.set_led_on_off(leds, OFF)


################################Test the AHRS##################################################
# Create an smubs object to read bytes
# mybus = smbus.SMBus(1)
# 
# # Create variables that contain the addresses for each sensor
# ahrs_address = 0x77
# 
# # Register for euler angle data is:
# # Euler angle data is 15 bytes total (12 of data)
# euler = 0x01
# 
# # Register for accelerometer data:
# # Accelerometer data is 15 bytes total (12 of data)
# accel = 0x27  # units: (G)
# 
# # Register for gyro data:
# # Gyro data is 15 bytes total (12 of data)
# gyro = 0x26  # units: (rad/s)

# Read accelerometer data
#print(mybus.read_i2c_block_data(ahrs_address, euler, 15))
#print(mybus.read_i2c_block_data(ahrs_address, accel, 15))
#print(mybus.read_i2c_block_data(ahrs_address, gyro, 15))

# First we need to tell the sensor that we want to send a command via:
# mybus.write_byte_data(ahrs_address, 0x98, 0xF6)
# 
# # Now we need to tell it which command to read
# mybus.read_byte_data(ahrs_address, 0x98)

# 
# while True:
#     read_euler = mybus.read_i2c_block_data(ahrs_address,euler,15)
#     print(read)
#     sleep(0.2)

###################Test the BrightPi#################################
# activate_led_routine(15)

###################Test the CO2Sensor################################
co2_data = get_co2_data(10)

             