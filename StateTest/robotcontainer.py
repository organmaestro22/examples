#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
from wpilib.interfaces import GenericHID

import commands2
import commands2.button

import constants


from commands.defaultdrive import DefaultDrive
from commands.halvedrivespeed import HalveDriveSpeed
from commands.curvatureDrive import CurvatureDrive

from subsystems.driveSubsystem import DriveSubsystem
from subsystems.state import State

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
        
        # State
        self.state = State()

        # Chooser
        self.chooser = wpilib.SendableChooser()

        # Add commands to the autonomous command chooser
        self.chooser.setDefaultOption("Simple Auto", 'A')
        self.chooser.addOption("Complex Auto", 'B')

        # Put the chooser on the dashboard
        wpilib.SmartDashboard.putData("Autonomous", self.chooser)

        self.configureButtonBindings()

        # set up default drive command
        self.drive.setDefaultCommand(
            DefaultDrive(
                self.drive,
                lambda: -self.driverController.getY(),
                lambda: self.driverController.getZ(),
            )
        )

    def mapButton(self, button, stateTrigger): # Maps a physical button to trigger a state change
        commands2.button.JoystickButton(self.driverController, button).onTrue(commands2.cmd.runOnce(lambda: self.state.handleButton(stateTrigger, True))).onFalse(commands2.cmd.runOnce(lambda: self.state.handleButton(stateTrigger, False)))

    def configureButtonBindings(self):
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """
        # BUTTONS - Buttons trigger states or commands
        self.mapButton(1, 'a')
        self.mapButton(2, 'b')
        self.mapButton(3, 'c')

        # STATES - States trigger commands
        # Invert the drivetrain direction
        commands2.button.Trigger(self.state.isDriveInverted).onTrue(
            commands2.cmd.runOnce(lambda: self.drive.invert())
        ).onFalse(
            commands2.cmd.runOnce(lambda: self.drive.invert())
        )
        # Set the drive command based on the drive state. This allows the drive to operate in multiple states
        commands2.button.Trigger(self.state.isDriveArcade).whileTrue(
            DefaultDrive(
                self.drive,
                lambda: -self.driverController.getY(),
                lambda: self.driverController.getZ(),
            )).whileFalse(
                CurvatureDrive(
                self.drive,
                lambda: -self.driverController.getY(),
                lambda: self.driverController.getZ(),
            ))
        
        commands2.button.Trigger(self.state.isDriveHalfSpeed).whileTrue(HalveDriveSpeed(self.drive))

    def getAutonomousCommand(self) -> str:
        return self.chooser.getSelected()
