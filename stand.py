#! /usr/bin/python3
# In the name of the most gracious and most merciful. May Allah be with us

# importing necessary modules

from gpiozero import AngularServo
import os

os.system("sudo pigpiod")
from gpiozero.pins.pigpio import PiGPIOFactory


# Creating factory instance for hardware PWM support

factory = PiGPIOFactory()

# stable values of each servo to start with

LEFT_WAIST = 105
LEFT_KNEE = 175
LEFT_ANKLE = 170

RIGHT_WAIST = 180
RIGHT_KNEE = 105
RIGHT_ANKLE = 135

# general speed of the servo

delay = 0.2

# servo initialization

left_waist = AngularServo(
    2,
    initial_angle=LEFT_WAIST,
    min_angle=0,
    max_angle=270,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025,
    frame_width=0.02,
    pin_factory=factory,
)

left_knee = AngularServo(
    17,
    initial_angle=LEFT_KNEE,
    min_angle=0,
    max_angle=270,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025,
    frame_width=0.02,
    pin_factory=factory,
)

left_ankle = AngularServo(
    4,
    initial_angle=LEFT_ANKLE,
    min_angle=0,
    max_angle=270,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025,
    frame_width=0.02,
    pin_factory=factory,
)


right_waist = AngularServo(
    16,
    initial_angle=RIGHT_WAIST,
    min_angle=0,
    max_angle=270,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025,
    frame_width=0.02,
    pin_factory=factory,
)

right_knee = AngularServo(
    20,
    initial_angle=RIGHT_KNEE,
    min_angle=0,
    max_angle=270,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025,
    frame_width=0.02,
    pin_factory=factory,
)

right_ankle = AngularServo(
    21,
    initial_angle=RIGHT_ANKLE,
    min_angle=0,
    max_angle=270,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025,
    frame_width=0.02,
    pin_factory=factory,
)
