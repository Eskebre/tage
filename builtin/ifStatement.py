def load():
    pass

name = "if"

def ifStatement(self, value1, op, value2, *args) -> None:
    """Executes a command if operation is true"""
    if self.comparativeOperation(value1, op, value2):
        # Rejoins all additional arguments and executes them
        self.executeCommand('\"'+'" "'.join(args)+'\"')
    return

def get_command():
    return name, ifStatement
