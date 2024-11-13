#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import typing
import commands2
from subsystems.driveSubsystem import DriveSubsystem
import navx
import math
import constants
import wpimath
from wpilib.shuffleboard import Shuffleboard
import time

def constrain(val, rmin, rmax):
    return min(rmax, max(val, rmin))

def isPositve(num):
    return abs(num) == num

def getAsPositive(angle, minA = -180, maxA = 180):
    return maxA + angle - minA

def getAsNegative(angle, minA = -180, maxA = 180):
    return minA + angle - maxA

def getClosestAngle(current, setpoint, minA = -180, maxA = 180):
    angle1 = (setpoint - getAsPositive(current)) if isPositve(setpoint) else (setpoint - getAsNegative(current))
    angle2 = setpoint - current
    return angle2 if abs(angle2) < abs(angle1) else angle1

class Drive(commands2.Command):
    def __init__(
        self,
        drive: DriveSubsystem,
        forward: typing.Callable[[], float],
        right: typing.Callable[[], float],
        twist: typing.Callable[[], float],
        navx: navx.AHRS
            ) -> None:
        

        self.drive = drive
        self.forward = forward
        self.right = right
        self.twist = twist
        self.navx = navx

        self.addRequirements(self.drive)
        self.addRequirements(self.navx)

        turnController = wpimath.controller.PIDController(
            constants.kP,
            constants.kI,
            constants.kD,
        )
        self.DC = 20 # degrees/s/s
        self.lastTime = None
        self.lastYaw = None

        self.tab = Shuffleboard.getTab("Turn PID")
        self.getP = self.tab.add("P", constants.kP).getEntry()
        self.getI = self.tab.add("I", constants.kI).getEntry()
        self.getD = self.tab.add("D", constants.kD).getEntry()
        turnController.enableContinuousInput(-180.0, 180.0)
        turnController.setTolerance(constants.kToleranceDegrees)

        self.turnController = turnController
        super().__init__()

    def getThrottle(self):
        return constrain(math.hypot(
            self.forward(), self.right()
            ) / (math.sqrt(2)/2), -1, 1)
        
    def getSetpoint(self):
        return math.degrees(
            math.atan2(
                -self.right(), -self.forward()
                        ))*179.9/180
    
    def getRotation(self, setpoint):
        return self.turnController.calculate(
                -self.navx.getYaw(), self.getSetpoint()
            )
        
    def execute(self):
        self.turnController.setP(self.getP.getFloat(constants.kP))
        self.turnController.setI(self.getI.getFloat(constants.kI))
        self.turnController.setD(self.getD.getFloat(constants.kD))
        
        throttle = self.getThrottle()
        setpoint = self.getSetpoint()
        current = self.navx.getYaw()

        # Calculate the robot's current rotoational speed
        if abs(self.right()) >= .2 or abs(self.forward()) >= .2:
            distanceToSetpoint = getClosestAngle(current, setpoint)
            if self.lastTime == None or self.lastYaw == None:
                self.lastTime = time.time()
                currentVelocity = 0
            else:
                currentVelocity = (current - self.lastYaw)/(time.time() - self.lastTime) # Degrees/s

            # Calculate the distance the robot will continue to rotoate if the motor is off
            coastTime = currentVelocity/self.DC
            coastDistance = currentVelocity * coastTime / 2
            
            # Calculate how much further the robot needs to go at the current speed to reach the setpoint, accounting for coasting occuring
            distanceToGo = round(distanceToSetpoint - coastDistance)
            print(distanceToGo)
            rotation = self.turnController.calculate(distanceToGo, 0)
            # print(self.getRotation(),self.getThrottle(),self.getSetpoint())
            self.drive.arcadeDrive(throttle, rotation)

        else: 
            self.drive.arcadeDrive(0, self.twist())