#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
from model.KeyboardThread import KeyboardThread
from model.Plotter import Plotter

# GPIO will warn if we clean up "unnecessarily"
GPIO.setwarnings(False)
# Cleaning up in case GPIOS have been preactivated
GPIO.cleanup()
# Z
coords = [[0, 0], [20, 20], [-20, 20], [20, 20], [0, 0], [-20, -20], [20, -20], [-20, -20], [0, 0]]


def main():
    traad = KeyboardThread()
    traad.start()

    hairy = Plotter()
    # Wait some time for GPIO
    time.sleep(0.5)
    print "Hit 'q' to quit"

    try:
        shouldRun = True
        coordIndex = 0
        currentCoord = [0, 0]
        hairy.toggleServo()
        while shouldRun:

            key = traad.getKey()
            if key == ord('q'):
                shouldRun = False

            hairy.goToPosition(currentCoord)

            coordIndex += 1
            if coordIndex >= len(coords):
                coordIndex = 0
                hairy.toggleServo()
                print "Done all coords"
                shouldRun = False
            currentCoord = coords[coordIndex]
    finally:
        # Cleaning up (motors can get hot if you dont)
        GPIO.cleanup()


main()
