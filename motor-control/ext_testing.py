
import pigpio
import time
import numpy as np
import sys
import Encoder

# define output pin
pi = pigpio.pi()
pin_out = 13
pi.set_mode(pin_out,pigpio.OUTPUT)

# define encoder
enc = Encoder.Encoder()

# get initial time
# time_i = time.perf_counter()
tick_i = pi.get_current_tick()

# set target duty cycle
dc_range = pi.get_PWM_range(pin_out)
duty_cycle = .5

pi.set_PWM_dutycycle(pin_out,dc_range*duty_cycle)


# get final time
# time_f = time.perf_counter()
tick_f = pi.get_current_tick()

# print("\nTime elapsed: ",time_f-time_i," s")
print("\nTime elapsed: ",pi.tickDiff(tick_i,tick_f)," ms")

# read encoder output from respective pins
print("Channel A: ",pi.read(3))
print("Channel B: ",pi.read(2))

print("Channel A: ",enc.read)
print("Channel B: ",enc.read)

# 1-second delay
time.sleep(1)