#!/usr/bin/env python
import RPi.GPIO as GPIO


class ServoMotor:
    # 7.5 should be center for SG90
    # (must've attached spinner slightly off-center)
    centerCycle = 7.9
    # Recommended maxLeft/maxRight is 5/10
    leftCycle = 4
    rightCycle = 13

    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(self.leftCycle)

    def __del__(self):
        # Not entirely necessary since stop is called on out of scope
        print "Cleaning (" + str(self.pin) + ")\r"
        self.pwm.stop()

    def center(self):
        # print "center"
        self.pwm.ChangeDutyCycle(self.centerCycle)

    def left(self):
        # print "left"
        self.pwm.ChangeDutyCycle(self.leftCycle)

    def right(self):
        # print "right"
        self.pwm.ChangeDutyCycle(self.rightCycle)
