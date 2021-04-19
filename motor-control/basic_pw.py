import pigpio
import time
import numpy as np
import sys

# define output pin
pi = pigpio.pi()
pin_out = 13
pi.set_mode(pin_out,pigpio.OUTPUT)

# get initial time
# time_i = time.perf_counter()
tick_i = pi.get_current_tick()

# set target pulsewidth
target_pw = int(sys.argv[1])
# this_pw = pi.get_servo_pulsewidth(pin_out)
# print("Current pulsewidth: ",this_pw)

pi.set_servo_pulsewidth(pin_out,target_pw)
print("Target pulsewidth: ",target_pw)


# get final time
# time_f = time.perf_counter()
tick_f = pi.get_current_tick()

# print("\nTime elapsed: ",time_f-time_i," s")
print("\nTime elapsed: ",pigpio.tickDiff(tick_i,tick_f)," ms")

# 1-second delay
time.sleep(1)