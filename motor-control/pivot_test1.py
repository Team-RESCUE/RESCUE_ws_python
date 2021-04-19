#!/usr/bin/python

import pigpio
import time
import numpy as np

pi = pigpio.pi()
pin_out = 13
pi.set_mode(pin_out, pigpio.OUTPUT)

# print ("mode: ", pi.get_mode(pin_out))
# print("setting to: ",pi.set_servo_pulsewidth(pin_out, 1500))
# print("set to: ",pi.get_servo_pulsewidth(pin_out))

# time.sleep(1)
time_i = time.perf_counter()

# print("setting to: ",pi.set_servo_pulsewidth(pin_out, 1090)) # level at 1090, or 27deg
target_pulsewidth = 1102 # level at 1102, or 30.6deg
this_pulsewidth = pi.get_servo_pulsewidth(pin_out)

# direction = (target_pulsewidth - this_pulsewidth)/np.absolute(target_pulsewidth-this_pulsewidth)

# pw_range = range(this_pulsewidth,target_pulsewidth+1,direction*22.18315018)

pw_range = np.linspace(this_pulsewidth,target_pulsewidth,num=10)

for pw in pw_range:
    pi.set_servo_pulsewidth(pin_out,pw)
    # print(pw)
#if pw_range[-1] != target_pulsewidth: #if last element is not target
#    pw_range = np.append(range(this_pulsewidth,target_pulsewidth,22.18315018),target_pulsewidth)

# print("set to: ",pi.get_servo_pulsewidth(pin_out))

time_f = time.perf_counter()

time.sleep(1)


print("time elapsed:",time_f-time_i,"s")

# print("setting to: ",pi.set_servo_pulsewidth(pin_out, 2000))
# print("set to: ",pi.get_servo_pulsewidth(pin_out))
# time.sleep(1)

pi.stop()