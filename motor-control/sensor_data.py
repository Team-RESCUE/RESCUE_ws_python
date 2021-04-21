# Import necessary packages
import smbus
import time
from scd30_i2c import SCD30
from brightpi import *


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
                print(f"CO2: {m[0]:.2f}ppm")
                next_time = time.time()
                time.sleep(2)
            else:
                 time.sleep(0.2)
            
            if (next_time - current_time) >= time_on:
                break
                 
    scd30.stop_periodic_measurement()
    brightPi.set_led_on_off(leds, OFF)
    return co2


###################Test the CO2Sensor################################
co2_data = get_co2_data(10)
print(co2_data)

             