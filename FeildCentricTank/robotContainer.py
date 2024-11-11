#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
from wpilib.interfaces import GenericHID

import commands2
import commands2.button
import navx

import constants

from subsystems.driveSubsystem import DriveSubsystem
from commands.driveCommand import Drive
from commands.restZero import ResetZero
from subsystems.turnPID import turnPID

class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:
        # The driver's controller
        # self.driverController = wpilib.XboxController(constants.kDriverControllerPort)
        self.driverController = wpilib.Joystick(constants.kDriverControllerPort)

        # The robot's subsystems
        self.drive = DriveSubsystem()

        # Navx
        self.navx = navx.AHRS.create_spi()
        # Chooser
        self.chooser = wpilib.SendableChooser()
        self.turnPID = turnPID()
        
        # State

        # Add commands to the autonomous command chooser
        self.chooser.setDefaultOption("Simple Auto", 'A')
        self.chooser.addOption("Complex Auto", 'B')

        # Put the chooser on the dashboard
        wpilib.SmartDashboard.putData("Autonomous", self.chooser)

        self.configureButtonBindings()

        # set up default drive command
        self.drive.setDefaultCommand(
            Drive(
                self.drive,
                lambda: -self.driverController.getX(),
                lambda: self.driverController.getY(),
                lambda: self.driverController.getZ(),
                self.navx
            )
        )

    def configureButtonBindings(self):
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """

        commands2.button.JoystickButton(self.driverController, 2).onTrue(ResetZero(self.navx))
            
    def getAutonomousCommand(self) -> str:
        return self.chooser.getSelected()
