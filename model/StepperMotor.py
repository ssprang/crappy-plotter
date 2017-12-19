#!/usr/bin/env python

import RPi.GPIO as GPIO
import math


# Define advanced sequence as shown in manufacturers datasheet
Seq = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]
StepsPerMm = 6000 / 180


class StepperMotor:

    # Position of thread in step counts
    currentPosition = 0
    targetPosition = 0
    # Current position in Seq
    motorCycle = 0

    def __init__(self, pins, motorCoord=[0, 0], penOffset=[0, 0], motorNr = -1):
        self.forwardPins = pins
        self.backwardPins = list(reversed(pins))
        self.motorCoord = motorCoord
        self.penOffset = penOffset
        self.currentPosition = self.getThreadPositionSteps([0, 0])
        self.targetPosition = self.currentPosition
        self.motorNr = motorNr # Only for debugging
        self.clear(self.forwardPins)

    def __del__(self):
        # Setting pins to low again (motors can get hot if you dont)
        print "Cleaning (" + ",".join(str(pin) for pin in self.forwardPins) + ")\r"
        self.clear(self.forwardPins)

    def setCurrentPosition(self, newPosition):
        self.currentPosition = newPosition

    def setTargetPosition(self, newPosition):
        self.targetPosition = newPosition

    def setTargetCoordinate(self, coord):
        self.targetPosition = self.getThreadPositionSteps(coord)
        
    # Returns distance in number of steps to reach specified coord
    def stepDistanceTo(self, coord):
        dist = abs(self.getThreadPositionSteps(coord) - self.currentPosition)
        return dist

    def getThreadPosition(self, coord):
        distX = self.motorCoord[0] - coord[0] + self.penOffset[0]
        distY = self.motorCoord[1] - coord[1] + self.penOffset[1]
        return math.sqrt(distX * distX + distY * distY)

    def getThreadPositionSteps(self, coord):
        return round(self.getThreadPosition(coord) * StepsPerMm)

    def hasArrived(self):
        return self.currentPosition == self.targetPosition

    def step(self):
        if self.currentPosition < self.targetPosition:
            self.backwards()
            self.currentPosition += 1
        elif self.currentPosition > self.targetPosition:
            self.forward()
            self.currentPosition -= 1

    def forward(self):
        self.moveAllPins(self.forwardPins)

    def backwards(self):
        self.moveAllPins(self.backwardPins)

    def moveAllPins(self, pins):
        for pin in range(0, 4):
            xpin = pins[pin]
            value = Seq[self.motorCycle][pin]
            self.movePin(xpin, value)
        self.motorCycle += 1
        # If we reach the end of the sequence start again
        if self.motorCycle == len(Seq):
            self.motorCycle = 0
        if self.motorCycle < 0:
            self.motorCycle = len(Seq)

    @staticmethod
    def movePin(pin, sequence):
        if sequence != 0:
            GPIO.output(pin, True)
        else:
            GPIO.output(pin, False)

    @staticmethod
    def clear(pins):
        # Use BCM GPIO references
        # instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)
