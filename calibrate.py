#!/usr/bin/env python

import time
import curses
import RPi.GPIO as GPIO
from model.StepperMotor import StepperMotor
from model.KeyboardThread import KeyboardThread

# Be sure you are setting pins accordingly
# GPIO10,GPIO9,GPIO11,GPI25
StepPins1 = [10, 9, 11, 25]
StepPins2 = [6, 13, 19, 26]
StepPins3 = [12, 16, 20, 21]
StepPins4 = [4, 17, 27, 22]

# GPIO will warn if we clean up "unnecessarily"
GPIO.setwarnings(False)
# Cleaning up in case GPIOS have been preactivated
GPIO.cleanup()


def main():

    motors = [
        StepperMotor(StepPins1),
        StepperMotor(StepPins2),
        StepperMotor(StepPins3),
        StepperMotor(StepPins4)
    ]

    # Wait some time for GPIO
    time.sleep(0.5)
    traad = KeyboardThread()
    traad.start()
    try:
        shouldRun = True
        backwards = False
        runMotor1 = False
        runMotor2 = False
        runMotor3 = False
        runMotor4 = False

        while shouldRun:
            # Each iteration moves motor one step
            # 28BYJ-48 w cannot move faster than 0.0010 per step
            time.sleep(0.0015)

            if runMotor1:
                motors[0].backwards() if backwards else motors[0].forward()
            if runMotor2:
                motors[1].backwards() if backwards else motors[1].forward()
            if runMotor3:
                motors[2].backwards() if backwards else motors[2].forward()
            if runMotor4:
                motors[3].backwards() if backwards else motors[3].forward()

            key = traad.getKey()
            if key == ord('q'):
                shouldRun = False
            if key == ord('b'):
                backwards = True
            if key == ord('f'):
                backwards = False

            # Toggle motor on/off per key press
            if key == curses.KEY_LEFT:
                runMotor1 = not runMotor1
            elif key == curses.KEY_RIGHT:
                runMotor2 = not runMotor2
            elif key == curses.KEY_UP:
                runMotor3 = not runMotor3
            elif key == curses.KEY_DOWN:
                runMotor4 = not runMotor4
    finally:
        # Cleaning up (motors can get hot if you dont)
        GPIO.cleanup()


main()
