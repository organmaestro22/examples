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

def constrain(val, rmin, rmax):
    return min(rmax, max(val, rmin))

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
    
    def getRotation(self):
        return self.turnController.calculate(
                -self.navx.getYaw(), self.getSetpoint()
            )
        
    def execute(self):
        self.turnController.setP(self.getP.getFloat(constants.kP))
        self.turnController.setI(self.getI.getFloat(constants.kI))
        self.turnController.setD(self.getD.getFloat(constants.kD))

        if abs(self.right()) >= .2 or abs(self.forward()) >= .2:
            # print(self.getRotation(),self.getThrottle(),self.getSetpoint())
            self.drive.arcadeDrive(self.getThrottle(), self.getRotation())

        else: 
            self.drive.arcadeDrive(0, self.twist())