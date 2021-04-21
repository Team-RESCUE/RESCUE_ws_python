# Import necessary packages
import smbus
import time
import board
import busio
import adafruit_scd30
from brightpi import *

def get_co2_and_LED(time_on):
    # We will need to adjust time_on based on how long the pan/tilt routine takes
    brightPi = BrightPi()

    # Reset the brightpi to ensure it's in its original state
    brightPi.reset()
    # Create an array for the LEDS - lets start with 6
    leds = [1,4]
    # Idea with this one is to collect the co2 data during our pan and tilt routine
    i2c = busio.I2C(board.SCL, board.SDA)
    scd = adafruit_scd30.SCD30(i2c)

    # Create the measurement interval
    scd.measurement_interval = 4
    # Set up the self calibration
    scd.self_calibration_enabled = True
    current_time = time.time()
    co2 = []
    # Turn on LEDS
    brightPi.set_led_on_off(leds, ON)
    while True:
        data = scd.data_available
        if data:
            co2.append(scd.CO2)
            print(scd.CO2)
            time.sleep(0.5)

        next_time = time.time()
        if (next_time - current_time) >= time_on:
            break
    brightPi.set_led_on_off(leds, OFF)
    return co2
    


co2_data = get_co2_and_LED(15)
