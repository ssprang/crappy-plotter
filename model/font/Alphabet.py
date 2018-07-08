#!/usr/bin/env python

from model.font.Character import Character

Scale = 5
# Defines set of Characters with coordinates
class Alphabet:

    def __init__(self):
        self.chars = {
            ' ': Character([], 2, 0),
            'A': Character([[[-1, -2], [-1, 0], [1, 0], [1, -2]], [[-1, -1], [1, -1]]], 2, 2),
            'B': Character([[[-1, -2], [-1, 0], [0, 0], [1, -0.5], [0, -1], [-1, -1], [0, -1], [1, -1.5], [0, -2], [-1, -2]]], 2, 2),
            'C': Character([[[1, -2], [-1, -2], [-1, 0], [1, -0]]], 2, 2),
            'D': Character([[[1, -1], [-1, -2], [-1, 2], [1, 1], [1, -1]]], 2, 4),
            'E': Character([[[1, -2], [-1, -2], [-1, 0], [1, 0]], [[-1, -1], [1, -1]]], 2, 2),
            'G': Character([[[0, 0], [1, 0], [1, -1], [0, -2], [-1, -1], [-1, 1], [0, 2], [1, 1]]], 2, 4),
            'H': Character([[[-1, -2], [-1, 0]], [[1, -2], [1, 0]], [[-1, -1], [1, -1]]], 2, 2),
            'I': Character([[[0, 2], [0, -2]]], 2, 2),
            'i': Character([[[0, 0], [0, -2]]], 2, 2),
            'J': Character([[[-1, 2], [1, 2], [1, -1], [0, -2], [-1, -1]]], 2, 4),
            'K': Character([[[-1, -2], [-1, 0]], [[1, -2], [-1, -1], [1, 0]]], 2, 2),
            'L': Character([[[-1, 2], [-1, -2], [1, -2]]], 2, 4),
            'M': Character([[[-1, -2], [-1, 0], [0, -1], [1, 0], [1, -2]]], 2, 2),
            'N': Character([[[-1, -2], [-1, 0], [1, -2], [1, 0]]], 2, 2),
            'O': Character([[[1, -1], [0, -2], [-1, -1], [-1, 1], [0, 2], [1, 1], [1, -1]]], 2, 4),
            'o': Character([[[1, 0], [-1, 0], [-1, -2], [1, -2], [1, 0]]], 2, 2),
            'P': Character([[[-1, -2], [-1, 0], [1, 0], [1, -1], [-1, -1]]], 2, 2),
            'R': Character([[[-1, -2], [-1, 0], [1, 0], [1, -1], [-1, -1], [1, -2]]], 2, 2),
            'S': Character([[[-1, -2], [1, -2], [1, -1], [-1, -1], [-1, 0], [1, 0]]], 2, 2),
            'T': Character([[[-1, 0], [1, 0]], [[0, -2], [0, 0]]], 2, 2),
            'U': Character([[[-1, 2], [-1, -1], [0, -2], [1, -1], [1, 2]]], 2, 4),
            'Z': Character([[[1, -2], [-1, -2], [1, 0], [-1, 0]]], 2, 2),
            'Y': Character([[[0, -2], [0, -1], [-1, 0]], [[0, -1], [1, 0]]], 2, 2),
            'a': Character([[[-1, 0], [1, 0], [1, -2], [-1, -2], [-1, -1], [1, -1]], [[0, 2], [0, 1], [1, 1], [1, 2], [0, 2]]], 2, 4),
            '0': Character([[[-1, 0], [-1, -2], [1, -2], [1, 0], [-1, 0]], [[-1, 2], [-1, 1]], [[1, 2], [1, 1]]], 2, 4),
            '+': Character([[[0, -2], [0, 0]], [[-1, -1], [1, -1]]], 2, 2),
            '!': Character([[[0, 2], [0,0]], [[0, -1], [0, -2]]], 2, 4)
        }

    def getCharacter(self, char, offset):
        print "Printing char " + str(char) + "\r"
        charModel = self.chars[char]
        newChar = Character([], charModel.widht*Scale, charModel.height*Scale)
        for coordList in charModel.coords:
            newCoordList = []
            for coord in coordList:
                newX = (coord[0]*Scale) + offset[0]
                newY = (coord[1]*Scale) + offset[1]
                newCoordList.append([newX, newY])
            newChar.coords.append(newCoordList)

        return newChar
