import commands2
import constants

class State(commands2.Subsystem):
    def __init__(self):
        super().__init__()

        self.driveState = constants.kDefaultDriveState
        self.driveInvState = constants.kDefaultDriveInvState
        self.halfSpeedState = constants.kDefaultHalfSpeedState

    def isDriveArcade(self):
        #print(self.driveState)
        return self.driveState
    
    def isDriveInverted(self):
        return self.driveInvState
    
    def isDriveHalfSpeed(self):
        return self.halfSpeedState != 0
    
    def handleButton1(self):
        print("Button 1")
        self.driveState = not self.driveState

    def handleButton2(self):
        print("Button 2")
        self.driveInvState = not self.driveInvState
    
    def handleButton3(self, pressed):
        print("Button 3")
        if pressed: self.halfSpeedState = 1
        else: self.halfSpeedState = 0