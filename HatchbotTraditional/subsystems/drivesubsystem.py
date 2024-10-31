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

        self.left1 = ctre.WPI_VictorSPX(constants.kLeftMotor1ID)
        self.left2 = ctre.WPI_VictorSPX(constants.kLeftMotor2ID)
        self.right1 = ctre.WPI_VictorSPX(constants.kRightMotor1ID)
        self.right2 = ctre.WPI_VictorSPX(constants.kRightMotor2ID)

        # The robot's drive
        self.drive = wpilib.drive.DifferentialDrive(
            wpilib.MotorControllerGroup(self.left1, self.left2),
            wpilib.MotorControllerGroup(self.right1, self.right2),
        )

    def arcadeDrive(self, fwd: float, rot: float) -> None:
        """
        Drives the robot using arcade controls.

        :param fwd: the commanded forward movement
        :param rot: the commanded rotation
        """
        self.drive.arcadeDrive(fwd, rot)

    def setMaxOutput(self, maxOutput: float):
        """
        Sets the max output of the drive. Useful for scaling the
        drive to drive more slowly.
        """
        self.drive.setMaxOutput(maxOutput)
