#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import wpilib
import wpilib.drive
import phoenix5 as ctre

import constants


class DriveSubsystem(commands2.Subsystem):
    def __init__(self) -> None:
        super().__init__()
        if wpilib.RobotBase.isSimulation():
            self.left1 = wpilib.PWMVictorSPX(1)
            self.right1 = wpilib.PWMVictorSPX(3)
            self.drive = wpilib.drive.DifferentialDrive(
                self.left1, self.right1
                )
            
        else:
            self.left1 = ctre.WPI_VictorSPX(constants.kLeftMotor1ID)
            self.left2 = ctre.WPI_VictorSPX(constants.kLeftMotor2ID)
            self.right1 = ctre.WPI_VictorSPX(constants.kRightMotor1ID)
            self.right2 = ctre.WPI_VictorSPX(constants.kRightMotor2ID)
            self.left = wpilib.MotorControllerGroup(self.left1, self.left2)
            self.right = wpilib.MotorControllerGroup(self.right1, self.right2)
            self.left.setInverted(True)
            # The robot's drive
            self.drive = wpilib.drive.DifferentialDrive(
                self.left,
                self.right,
            )
        self.isInverted = False
        self.isFlagged = False
        self.flagdata = None
        self.drive.setMaxOutput(.75)

    def arcadeDrive(self, fwd: float, rot: float) -> None:
        """
        Drives the robot using arcade controls.

        :param fwd: the commanded forward movement
        :param rot: the commanded rotation
        """
        #print(self.isInverted)
        if self.isInverted: fwd = -fwd # invert the direction of the throttle if in inverted mode

        self.drive.arcadeDrive(fwd, rot)

    def curvatureDrive(self, fwd: float, rot: float) -> None:
        """
        Drive using Curvature Drive

        Args:
            fwd (float): Throttle
            rot (float): Steering
            """
        if self.isInverted: fwd = -fwd # invert the direction of the throttle if in inverted mode

        self.drive.curvatureDrive(fwd, rot, True)

    def setMaxOutput(self, maxOutput: float):
        """
        Sets the max output of the drive. Useful for scaling the
        drive to drive more slowly.
        """
        self.drive.setMaxOutput(maxOutput)
    
    def invert(self, isInverted: bool = None):
        """
        Invert the direction of the throttle

        Args:
            isInverted (bool): Whether or not the throttle is inverted
        """
        if isInverted == None: isInverted = not self.isInverted
        self.isInverted = isInverted

    def flag(self, flagdata):
        self.isFlagged = True
        self.flagdata = flagdata