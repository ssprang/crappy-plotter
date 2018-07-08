#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
from model.KeyboardThread import KeyboardThread
from model.Plotter import Plotter

# GPIO will warn if we clean up "unnecessarily"
from model.font.Alphabet import Alphabet

GPIO.setwarnings(False)
# Cleaning up in case GPIOS have been preactivated
GPIO.cleanup()
alphabet = Alphabet()


def main():
    traad = KeyboardThread()
    traad.start()

    hairy = Plotter()
    # Wait some time for GPIO
    time.sleep(0.5)
    print "Hit 'q' to quit\r"

    try:
        currentCoord = [-20, 25]
        hairy.goToPosition(currentCoord)
        stringToPrint = "KRYA"
        for c in stringToPrint:
            key = traad.getKey()
            if key == ord('q'):
                return
            writeLetter(hairy, c, currentCoord)

        currentCoord = [-30, 0]
        hairy.goToPosition(currentCoord)
        stringToPrint = "Pa DIG"
        for c in stringToPrint:
            key = traad.getKey()
            if key == ord('q'):
                return
            writeLetter(hairy, c, currentCoord)

        currentCoord = [-30, -25]
        hairy.goToPosition(currentCoord)
        stringToPrint = "SiMoNE!"
        for c in stringToPrint:
            key = traad.getKey()
            if key == ord('q'):
                return
            writeLetter(hairy, c, currentCoord)

        #currentCoord = [-40, -45]
        #hairy.goToPosition(currentCoord)
        #stringToPrint = "+ ROBOT"
        #for c in stringToPrint:
        #    key = traad.getKey()
        #    if key == ord('q'):
        #        return
        #    writeLetter(hairy, c, currentCoord)

    finally:
        hairy.goToPosition([0, 0])
        # Cleaning up (motors can get hot if you dont)
        GPIO.cleanup()
        print "Done!\r"
        time.sleep(2)


def writeLetter(hairy, character, currentCoord):
    char = alphabet.getCharacter(character, currentCoord)
    for coordList in char.coords:
        onFirstLetter = True
        for coord in coordList:
            hairy.goToPosition(coord)
            if onFirstLetter:
                hairy.toggleServo()
                onFirstLetter = False
        hairy.toggleServo()
    currentCoord[0] = currentCoord[0] + char.widht + 3


main()
