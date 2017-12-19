#!/usr/bin/env python
# Hello my name is Hairy Plotter
import math
import time

from model.ServoMotor import ServoMotor
from model.StepperMotor import StepperMotor

# Be sure you are setting pins accordingly
# GPIO10,GPIO9,GPIO11,GPI25
StepPins1 = [10, 9, 11, 25]
StepPins2 = [6, 13, 19, 26]
StepPins3 = [12, 16, 20, 21]
StepPins4 = [4, 17, 27, 22]

ServoPin = 23

# Each iteration moves motor one step
# 28BYJ-48 w cannot move faster than 0.0010 per step 
SleepTime = 0.0015

# Depends on spool radius
StepsPerMm = 6000 / 180
# mm per step with arrow keys
StepSize = 5
# Defines center as 0, max right 105, max left -105
AreaLimitX = 105
# Defines center as 0, max top 148, max bottom -148
AreaLimitY = 148


class Plotter:

    # Defines motors as set of 4 StepperMotor(s) in specific order
    def __init__(self):
        self.posX = 0
        self.posY = 0
        self.motors = [
            StepperMotor(StepPins1, [132, -140], [29, -29], 1),
            StepperMotor(StepPins2, [-132, 140], [-29, 29], 2),
            StepperMotor(StepPins3, [-106, -165], [-29, 29], 3),
            StepperMotor(StepPins4, [106, 165], [29, 29], 4)
        ]
        self.servoIsUp = True
        self.servo = ServoMotor(ServoPin)
        self.servo.center()

    def moveLeft(self):
        self.posX -= StepSize
        if self.posX < -AreaLimitX:
            self.posX = -AreaLimitX
        self.goToPosition([self.posX, self.posY])

    def moveRight(self):
        self.posX += StepSize
        if self.posX > AreaLimitX:
            self.posX = AreaLimitX
        self.goToPosition([self.posX, self.posY])

    def moveDown(self):
        self.posY -= StepSize
        if self.posY < -AreaLimitY:
            self.posY = -AreaLimitY
        self.goToPosition([self.posX, self.posY])

    def moveUp(self):
        self.posY += StepSize
        if self.posY > AreaLimitY:
            self.posY = AreaLimitY
        self.goToPosition([self.posX, self.posY])

    # Deprecated!
    def moveMotors(self):
        hasArrived = True
        for motorNumber in range(0, len(self.motors)):
            self.motors[motorNumber].setTargetPosition(self.getThreadPosition(motorNumber + 1))
            self.motors[motorNumber].step()
            hasArrived = hasArrived and self.motors[motorNumber].hasArrived()
        return hasArrived

    # Going to a destination coordinate
    def goToPosition(self, destination):
        motorStepsToTake = []
        for motor in self.motors:
            motorStepsToTake.append(motor.stepDistanceTo(destination))
            motor.setTargetCoordinate(destination)
        motorStepsTaken = [0] * len(self.motors)
        maxDist = int(max(motorStepsToTake) + 0.5)
        for i in range(0, maxDist):
            for motorNumber in range(0, len(self.motors)):
                expectedStepsTaken = int((i * motorStepsToTake[motorNumber]) / maxDist + 0.5)
                if motorStepsTaken[motorNumber] < expectedStepsTaken:
                    self.motors[motorNumber].step()
                    motorStepsTaken[motorNumber] += 1
                    if motorStepsTaken[motorNumber] < expectedStepsTaken:
                        print "Should not happen!"
            time.sleep(SleepTime)

        self.posX = destination[0]
        self.posY = destination[1]

        return True

    # Deprecated!
    def getThreadPosition(self, motorNr):
        motorX = AreaLimitX
        if motorNr == 2 or motorNr == 3:
            motorX = -motorX
        motorY = AreaLimitY
        if motorNr == 1 or motorNr == 3:
            motorY = -motorY
        distX = self.posX - motorX
        distY = self.posY - motorY
        dist = math.sqrt(distX * distX + distY * distY)
        return round(dist * StepsPerMm)

    def toggleServo(self):
        if self.servoIsUp:
            self.servo.left()
            self.servoIsUp = False
        else:
            self.servo.center()
            self.servoIsUp = True
        time.sleep(0.5)
