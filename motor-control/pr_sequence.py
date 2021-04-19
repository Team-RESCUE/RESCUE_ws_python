# import pigpio
import time
import numpy as np
import sys

# define output pins
# pi = pigpio.pi()
pins_out = [13,5]

# get initial pulsewidths
this_pws = [int(sys.argv[1]), int(sys.argv[2])]

# set target pulsewidths
target_pws = [int(sys.argv[3]), int(sys.argv[4])]

# get initial time
time_i = time.perf_counter()

for i in range(len(pins_out)):
    # pi.set_mode(pins_out[i],pigpio.OUTPUT)
    # pi.set_servo_pulsewidth(pins_out[i],target_pws[i])
    print("Current: ",this_pws[i],"    Target: ",target_pws[i])

    pw_diff = np.absolute(np.subtract(target_pws[i],this_pws[i]))
    direction = (target_pws[i]-this_pws[i])/pw_diff
    
    while pw_diff > 20:
        # pi.set_servo_pulsewidth(pins_out[i],this_pws[i]+direction*pw_diff/2)
        # this_pws[i] = pi.get_servo_pulsewidth(pins_out[i])
        this_pws[i] = this_pws[i] + direction*pw_diff/2
        print(this_pws[i])

        pw_diff = np.absolute(this_pws[i]-target_pws[i])
    
    # pi.set_servo_pulsewidth(pins_out[i],target_pws[i])
    print("Arrived at ",target_pws[i])

# get final time
time_f = time.perf_counter()
print("\nTime elapsed: ",time_f-time_i," s")