#!/usr/bin/env python

import time
import curses
import RPi.GPIO as GPIO
from model.KeyboardThread import KeyboardThread
from model.Plotter import Plotter

# GPIO will warn if we clean up "unnecessarily"
GPIO.setwarnings(False)
# Cleaning up in case GPIOS have been preactivated
GPIO.cleanup()


def main():
    traad = KeyboardThread()
    traad.start()

    hairy = Plotter()
    # Wait some time for GPIO
    time.sleep(0.5)
    print "Hit 'q' to quit, 'u' to toggle servo and arrow keys to move plotter."

    try:
        shouldRun = True

        while shouldRun:
            # Each iteration moves motor one step
            # 28BYJ-48 w cannot move faster than 0.0010 per step 
            time.sleep(0.0010)
            key = traad.getKey()
            if key == ord('q'):
                shouldRun = False
            if key == ord('u'):
                hairy.toggleServo()
            if key == curses.KEY_RIGHT:
                hairy.moveRight()
            elif key == curses.KEY_LEFT:
                hairy.moveLeft()
            elif key == curses.KEY_DOWN:
                hairy.moveDown()
            elif key == curses.KEY_UP:
                hairy.moveUp()

    finally:
        # Cleaning up (motors can get hot if you dont)
        GPIO.cleanup()


main()
