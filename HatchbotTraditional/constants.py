#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

#
# The constants module is a convenience place for teams to hold robot-wide
# numerical or boolean constants. Don't use this for any other purpose!
#

import math
import wpilib

# Motors
kLeftMotor1ID = 1
kLeftMotor2ID = 2
kRightMotor1ID = 3
kRightMotor2ID = 4

kWheelDiameterInches = 6

# Autonomous
kAutoDriveDistanceInches = 60
kAutoBackupDistanceInches = 20
kAutoDriveSpeed = 0.5

# Operator Interface
kDriverControllerPort = 0

# Physical parameters
kDriveTrainMotorCount = 2
kTrackWidth = 0.381 * 2
kGearingRatio = 8
kWheelRadius = 0.0508