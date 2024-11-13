import math
import wpilib
import wpimath.kinematics
import wpimath.geometry
import wpimath.controller
import wpimath.trajectory
import rev
import phoenix5 as ctre


kWheelRadius = 0.0508
kModuleMaxAngularVelocity = math.pi
kModuleMaxAngularAcceleration = math.tau


class SwerveModule:
    def __init__(self, driveid, steerid, P, I, D):
        self.drive = ctre.WPI_VictorSPX(driveid)
        self.turn = rev.CANSparkMax(steerid, rev.CANSparkLowLevel.MotorType.kBrushless)
        self.turnEncoder = self.turn.getEncoder()
        self.turningPIDController = wpimath.controller.ProfiledPIDController(
            P,
            I,
            D,
            wpimath.trajectory.TrapezoidProfile.Constraints(
                kModuleMaxAngularVelocity,
                kModuleMaxAngularAcceleration,
            ),
        )
        
        