import commands2
import constants

class State(commands2.Subsystem):
    def __init__(self):
        super().__init__()

        self.driveState = constants.kDefaultDriveState
        self.driveInvState = constants.kDefaultDriveInvState
        self.halfSpeedState = constants.kDefaultHalfSpeedState
        # Each drive state 'remembers' if it is in halfspeed or is inverted
        self.driveState0Configs = (self.driveInvState, self.halfSpeedState)
        self.driveState1Configs = (self.driveInvState, self.halfSpeedState)

    def isDriveArcade(self):
        #print(self.driveState)
        return self.driveState == 0
    
    def isDriveInverted(self):
        return self.driveInvState
    
    def isDriveHalfSpeed(self):
        return self.halfSpeedState != 0
    
    def handleButton(self, button, pressed):
        if button == 'a' and pressed:
            print("Button A")
            if self.driveState == 0:
                self.driveState0Configs = (self.driveInvState, self.halfSpeedState)
                self.driveInvState, self.halfSpeedState = self.driveState1Configs
                self.driveState = 1
            elif self.driveState == 1:
                self.driveState1Configs = (self.driveInvState, self.halfSpeedState)
                self.driveInvState, self.halfSpeedState = self.driveState0Configs
                self.driveState = 0

        if button == 'b' and pressed:
            print("Button B")
            self.halfSpeedState = not self.halfSpeedState

        if button == 'c' and pressed:
            print("Button C")
            self.driveInvState = not self.driveInvState