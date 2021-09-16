#! /usr/bin/python3
# In the name of the most gracious and most merciful. May Allah be with us

# importing necessary modules

import threading
from gpiozero import AngularServo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
import sys
import signal
import os
import subprocess

# PID of current python process

TERMINATION_FLAG = False

# Signal Handler Function

def terminate(signal_number, frame):
    global TERMINATION_FLAG
    TERMINATION_FLAG = True
    print(f"SIGINT received: {signal_number}")
    print(f"SIGINT frame: {frame}")

# Custom Signal Handler

signal.signal(signal.SIGINT, terminate)


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


def ankle1():
    while left_ankle.angle <= 200: ### 170 to 200 ## 30
        if TERMINATION_FLAG:
            while left_ankle.angle >= 170:
                left_ankle.angle -= 1
                sleep(delay)
        left_ankle.angle += 1
        print(left_ankle.angle)
        sleep(delay)


def ankle2():
    while right_ankle.angle >= 110: ### 135 to 110 ## 25
        if TERMINATION_FLAG:
            while right_ankle.angle <= 135:
                right_ankle.angle += 1
                sleep(delay)
        right_ankle.angle -= 1
        sleep(delay * 1.6)


def ankle3():
    while right_ankle.angle <= 155:  ### 135 to 155 ## 20
        right_ankle.angle += 1
        sleep(delay)


def ankle4():
    while left_ankle.angle >= 145:  ### 180 to 145 ## 35
        left_ankle.angle = left_ankle.angle - 1
        sleep(delay)


def ankle5():
    while left_ankle.angle <= 200:  ### 170 to 200 ## 30
        left_ankle.angle += 1
        sleep((delay * 1.5))


def ankle6():
    while right_ankle.angle >= 110:  ### 145 to 110 ## 35
        right_ankle.angle -= 1
        sleep(delay)


    


# Main function

def check_successful_termination():
    if not (right_ankle.angle > 134 and right_ankle.angle < 136):
        string = "espeak -ven+m7 'Failed to terminate right ankle properly' -p 30 -g 3"
        subprocess.run(string, shell=True, executable="/bin/bash")
    if not (right_knee.angle > 104 and right_knee.angle < 106):
        string = "espeak -ven+m7 'Failed to terminate right knee properly' -p 30 -g 3"
        subprocess.run(string, shell=True, executable="/bin/bash")
    if not (right_waist.angle > 179 and right_waist.angle < 181):
        string = "espeak -ven+m7 'Failed to terminate right waist properly' -p 30 -g 3"
        subprocess.run(string, shell=True, executable="/bin/bash")
    if not (left_ankle.angle > 169 and left_ankle.angle < 171):
        string = "espeak -ven+m7 'Failed to terminate left ankle properly' -p 30 -g 3"
        subprocess.run(string, shell=True, executable="/bin/bash")
    if not (left_knee.angle > 174 and left_knee.angle < 176):
        string = "espeak -ven+m7 'Failed to terminate left knee properly' -p 30 -g 3"
        subprocess.run(string, shell=True, executable="/bin/bash")
    if not (left_waist.angle > 104 and left_waist.angle < 106):
        string = "espeak -ven+m7 'Failed to terminate left waist properly' -p 30 -g 3"
        subprocess.run(string, shell=True, executable="/bin/bash")


def walk():


    ankle_thread1 = threading.Thread(target=ankle1)
    ankle_thread2 = threading.Thread(target=ankle2)
    ankle_thread3 = threading.Thread(target=ankle3)
    ankle_thread4 = threading.Thread(target=ankle4)
    ankle_thread5 = threading.Thread(target=ankle5)
    ankle_thread6 = threading.Thread(target=ankle6)

    ankle_thread1.start()
    ankle_thread2.start()
    ankle_thread1.join()
    ankle_thread2.join()

    if TERMINATION_FLAG:
        check_successful_termination()
        sys.exit()

    while left_ankle.angle >= 170: ### 200 to 170 ## 30
        left_ankle.angle -= 1
        sleep(delay / 2)

    if TERMINATION_FLAG:
        while right_ankle.angle <= 135:
            right_ankle.angle += 1
            sleep(delay)
        check_successful_termination()
        sys.exit()

    while left_waist.angle >= 60:  ### 105 to 60 ## 45
        if TERMINATION_FLAG:
            while left_waist.angle <= 105:
                left_waist.angle += 1
                sleep(delay)
            while right_ankle.angle <= 135:
                right_ankle.angle += 1
                sleep(delay)
            check_successful_termination()
            sys.exit()
        left_waist.angle -= 1
        sleep(delay)
    while left_knee.angle <= 185:  ### 175 to 185 ## 10
        if TERMINATION_FLAG:
            while left_knee.angle >= 175:
                left_knee.angle -= 1
                sleep(delay)
            while left_waist.angle <= 105:
                left_waist.angle += 1
                sleep(delay)
            while right_ankle.angle <= 135:
                right_ankle.angle += 1
                sleep(delay)
            check_successful_termination()
            sys.exit()
        left_knee.angle += 1
        sleep(delay)
    while right_knee.angle <= 140:  ### 105 to 140 ## 35
        right_knee.angle += 1
        sleep(delay)
    while left_ankle.angle <= 180:  ### 170 to 180 ## 10
        left_ankle.angle += 1
        sleep(delay)
    while right_ankle.angle <= 135:  ### 110 to 135 ## 25
        right_ankle.angle += 1
        sleep(delay)

    ankle_thread3.start()
    ankle_thread4.start()
    ankle_thread3.join()
    ankle_thread4.join()

    while left_knee.angle >= 175:  ### 185 to 175 ## 10
        left_knee.angle -= 1
        sleep(delay)
    

    while right_ankle.angle >= 145:  ### 155 to 145 ## 10
        right_ankle.angle -= 1
        sleep(delay)
    while left_waist.angle <= 105:  ### 60 to 105 ## 45
        left_waist.angle += 1
        sleep(delay)
    while right_knee.angle >= 105:  ### 140 to 105 ## 35
        right_knee.angle -= 1
        sleep(delay)

    if TERMINATION_FLAG:
        while right_ankle.angle >= 135:
            right_ankle.angle -= 1
            sleep(delay)
        while left_ankle.angle <= 170:
            left_ankle.angle += 1
            sleep(delay)
        check_successful_termination()
        sys.exit()

    """From here we will implement walking algorithm from the very first step
    just considering it in reverse i.e. left will be right and vice and versa"""
    while right_waist.angle <= 225:  ### 180 to 225 ## 45
        if TERMINATION_FLAG:
            while right_waist.angle >= 180:
                right_waist.angle -= 1
                sleep(delay)
            while right_ankle.angle >= 135:
                right_ankle.angle -= 1
                sleep(delay)
            while left_ankle.angle <= 170:
                left_ankle.angle += 1
                sleep(delay)
            check_successful_termination()
            sys.exit()
        right_waist.angle += 1
        sleep(delay)
    while right_knee.angle >= 95:  ### 105 to 95 ## 10
        if TERMINATION_FLAG:
            while right_knee.angle <= 105:
                right_knee.angle += 1
                sleep(delay)
            while right_waist.angle >= 180:
                right_waist.angle -= 1
                sleep(delay)
            while right_ankle.angle >= 135:
                right_ankle.angle -= 1
                sleep(delay)
            while left_ankle.angle <= 170:
                left_ankle.angle += 1
                sleep(delay)
            check_successful_termination()
            sys.exit()
        right_knee.angle -= 1
        sleep(delay)
    while left_knee.angle >= 140:  ### 175 to 140 ## 35
        left_knee.angle -= 1
        sleep(delay)
    while left_ankle.angle <= 170:
        left_ankle.angle += 1
        sleep(delay)

    ankle_thread5.start()
    ankle_thread6.start()
    ankle_thread5.join()
    ankle_thread6.join()

    
    while left_ankle.angle >= 175:
        left_ankle.angle -= 1
        sleep(delay)
    while right_knee.angle <= 105:
        right_knee.angle += 1
        sleep(delay)
    while right_waist.angle >= 180:
        right_waist.angle -= 1
        sleep(delay)
    while left_knee.angle <= 175:
        left_knee.angle += 1
        sleep(delay)
    # while right_waist.angle >= 180: ### DEEMED REDUNDANT
    #     right_waist.angle -= 1
    #     sleep(delay)

    if TERMINATION_FLAG:
        while right_ankle.angle <= 135:
            right_ankle.angle += 1
            sleep(delay)
        check_successful_termination()
        sys.exit()


if __name__ == "__main__":
    while True:
        walk()
