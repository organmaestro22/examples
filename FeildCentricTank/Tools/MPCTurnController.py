import math
from subsystems.driveSubsystem import DriveSubsystem
from navx import AHRS
import time

class MPCTurnController():
    def __init__(self, decelCoefficent, P):
        self.DC = decelCoefficent # Degrees/s/s
        self.P = P # Percent change in output to cause a change in velocity of 1 Degree/s
        self.currentOutput = 0
        self.lastTime = None
        self.last = None

    def update(self, current, setpoint):
        distanceToSetpoint = current - setpoint
        if not (self.lastTime or self.last):
            self.lastTime = time.time()
            currentVelocity = 0
        else:
            currentVelocity = (current - self.last)/(time.time() - self.lastTime) # Degrees/s

        # Calculate the distance the robot will go if the motor is coasting
        coastTime = currentVelocity/self.DC
        coastDistance = currentVelocity * coastTime / 2
        
        # Calculate how much further the robot needs to go at the current speed to reach the setpoint, accounting for coasting occuring
        distanceToGo = distanceToSetpoint - coastDistance

        
