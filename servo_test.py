#!/usr/bin/env python

import curses
import time
import RPi.GPIO as GPIO
from model.KeyboardThread import KeyboardThread
from model.ServoMotor import ServoMotor

# GPIO will warn if we clean up "unnecessarily"
GPIO.setwarnings(False)
# Cleaning up in case GPIOS have been preactivated
GPIO.cleanup()


def main():
    traad = KeyboardThread()
    traad.start()

    servo = ServoMotor(23)
    # Wait some time for GPIO
    time.sleep(0.5)

    try:
        shouldRun = True

        while shouldRun:
            time.sleep(0.0020)
            key = traad.getKey()
            if key == ord('q'):
                shouldRun = False
            if key == curses.KEY_RIGHT:
                print "got right"
                servo.right()
            elif key == curses.KEY_LEFT:
                servo.left()
            elif key == curses.KEY_DOWN:
                servo.center()
            elif key == curses.KEY_UP:
                servo.center()

    finally:
        # Cleaning up (motors can get hot if you dont)
        GPIO.cleanup()


main()
