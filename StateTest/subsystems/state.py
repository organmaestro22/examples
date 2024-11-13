import commands2
import constants
from wpilib.shuffleboard import Shuffleboard

class State(commands2.Subsystem):
    def __init__(self):
        super().__init__()

        self.driveState = constants.kDefaultDriveState
        self.driveInvState = constants.kDefaultDriveInvState
        self.halfSpeedState = constants.kDefaultHalfSpeedState

        # Each drive state 'remembers' if it is in halfspeed or is inverted
        self.driveState0Configs = (self.driveInvState, self.halfSpeedState)
        self.driveState1Configs = (self.driveInvState, self.halfSpeedState)

        # Shuffleboard widgets
        self.tab = Shuffleboard.getTab("State")
        self.driveModeWidget = self.tab.addPersistent("Drive Mode", "Default").getEntry()
        self.driveInvWidget = self.tab.addPersistent("Drive Inversion", "Default").getEntry()
        self.driveSpeedWidget = self.tab.addPersistent("Drive Speed", "Default").getEntry()

    def isDriveArcade(self):
        #print(self.driveState)
        return self.driveState == 0
    
    def isDriveInverted(self):
        return self.driveInvState
    
    def isDriveHalfSpeed(self):
        return self.halfSpeedState != 0
    
    def updateWidgets(self):
        # Update the displayed state values
        self.driveModeWidget.setString("Arcade" if self.driveState == 1 else "Curvature")
        self.driveInvWidget.setString("Yes" if self.driveInvState else "No")
        self.driveSpeedWidget.setString("1/2" if self.halfSpeedState else "3/4")


    def handleButton(self, button, pressed):
        if button == 'a' and pressed: # Change the drive mode
            print("Button A")
            if self.driveState == 0:
                self.driveState0Configs = (self.driveInvState, self.halfSpeedState)
                self.driveInvState, self.halfSpeedState = self.driveState1Configs
                self.driveState = 1
            elif self.driveState == 1:
                self.driveState1Configs = (self.driveInvState, self.halfSpeedState)
                self.driveInvState, self.halfSpeedState = self.driveState0Configs
                self.driveState = 0

        
        elif button == 'b' and pressed: # Toggle halfspeed
            print("Button B")
            self.halfSpeedState = not self.halfSpeedState

        elif button == 'c' and pressed: # Invert drive direction
            print("Button C")
            self.driveInvState = not self.driveInvState
        
        self.updateWidgets() # Update Shuffleboard to match the new state(s)