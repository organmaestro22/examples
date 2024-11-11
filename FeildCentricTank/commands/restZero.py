#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import navx

class ResetZero(commands2.Command):
    def __init__(
            self,
            navx: navx.AHRS
            ) -> None:
        super().__init__()

        self.navx = navx

        self.addRequirements(self.navx)
        self.done = False
        
    def initialize(self):
        self.navx.zeroYaw()
        self.done = True
    
    def isFinished(self) -> bool:
        return self.done
        