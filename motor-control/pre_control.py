import pigpio
import time
import numpy as np
import sys

# define output pins
pi = pigpio.pi()
pins_out = [13,12] # need some third pin for ext. control
# pivot_pinout = 13
# rot_pinout = 5
pi.set_mode(pins_out,pigpio.OUTPUT)

# get initial time
tick_i = pi.get_current_tick()

# get initial pulsewidths
this_pws = [pi.get_servo_pulsewidth(pins_out)]

# set target pulsewidths
target_pws = [int(sys.argv[1]), int(sys.argv[2])] #, int(sys.argv[3])]

# pi.set_servo_pulsewidth(pins_out,target_pws)

# loop to target pulsewidths
pw_diff = np.absolute(np.subtract(target_pws,this_pws)) 
pw_close = (pw_diff < 20).astype(int)

while np.sum(pw_close) < len(pw_close):
    active = pw_close != 1 # only modify pulsewidth if not close to target
    pi.set_servo_pulsewidth(pins_out[active], np.add(this_pws[active],target_pws[active])/2)
    this_pws = [pi.get_servo_pulsewidth(pins_out)]
    # this_pws = np.add(this_pws,pw_diff)/2
    pw_diff = np.absolute(np.subtract(target_pws,this_pws))
    pw_close = (pw_diff < 20).astype(int)

# final iteration to target pulsewidth
pi.set_servo_pulsewidth(pins_out,target_pws)

# get final time
tick_f = pi.get_current_tick()

# print statements
print("Pivot pulsewidth changed from ",this_pws[0]," to ",target_pws[0])
print("Rotation pulsewidth changed from ",this_pws[1]," to ",target_pws[1])

# 1-second delay
time.sleep(1)