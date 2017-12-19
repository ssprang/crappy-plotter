#!/usr/bin/env python
from model.font.Alphabet import Alphabet


def main():
    alpha = Alphabet()
    printAllCoords(alpha.getCharacter('Z', [10, 10]))
    print "-------"
    printAllCoords(alpha.getCharacter('Z', [0, 0]))


def printAllCoords(char):
    for coord in char.coords:
        print "Got coord " + str(coord)

main()
