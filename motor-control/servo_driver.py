import RPi.GPIO as GPIO


def interp_duty_cycle(angle):
    min_pulse = 0.5  # ms
    max_pulse = 2.5  # ms
    min_angle = 0  # degrees
    max_angle = 300  # degrees

    out_pulse = 0.5 + (angle - 0) * ((max_pulse - min_pulse)/(max_angle - min_angle))
    out_duty_cycle = out_pulse * 10  # percentage between 0 and 100
    return out_duty_cycle


def calc_duty_cycle_vec(angle_vec):
    duty_cycle_vec = list.copy(angle_vec)
    for i in range(0, len(angle_vec)):
        duty_cycle_vec[i] = interp_duty_cycle(angle_vec[i])

    return duty_cycle_vec


def pivot_servo():
    # Set io mode to broadcom
    GPIO.setmode(GPIO.BOARD)
    # # Set GPIO pin 19 as our output pin
    GPIO.setup(12, GPIO.OUT)

    angle_vec = [35, 21, 36, 8, 12, 85, 87, 52, 5, 32, 74, 1, 3, 15, 59, 66, 58, 41, 49, 26]

    duty_cycle_vec = calc_duty_cycle_vec(angle_vec)
    print(duty_cycle_vec)
    p = GPIO.PWM(12, duty_cycle_vec[0])
    p.start(1)
    p.ChangeDutyCycle(0)
    p.stop()


if __name__ == '__main__':
    pivot_servo()

