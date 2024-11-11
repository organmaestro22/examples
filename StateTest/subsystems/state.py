import commands2
import constants

class State(commands2.Subsystem):
    def __init__(self):
        super().__init__()

        self.driveState = constants.kDefaultDriveState
        self.driveInvState = constants.kDefaultDriveInvState
        self.speedState = constants.kDefaultSpeedState

    def isDriveArcade(self):
        #print(self.driveState)
        return self.driveState
    
    def isDriveInverted(self):
        return self.driveInvState
    
    def isDriveDifferentSpeed(self):
        return self.speedState != 0
    
    def handleButton1(self):
        self.driveState = not self.driveState

    def handleButton2(self):
        self.driveInvState = not self.driveInvState