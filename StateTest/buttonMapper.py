buttonsToMap = ["a", "b", "c","b"]
output = ""
for name in buttonsToMap:
    button = input(f"Button to map to {name}")
    output += f"commands2.button.JoystickButton(self.driverController, {button}).onTrue(commands2.cmd.runOnce(lambda: self.state.handleButton('{name}', True))).onFalse(commands2.cmd.runOnce(lambda: self.state.handleButton('{name}', False)))\n"
print(output)