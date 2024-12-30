def load(tage):
    return True

name = "if"

def ifStatement(tage, value1, op, value2, *args) -> None:
    """Executes a command if operation is true"""
    if tage.comparativeOperation(value1, op, value2):
        # Rejoins all additional arguments and executes them
        tage.executeCommand('\"'+'" "'.join(args)+'\"')
    return

def get_command():
    return {name: ifStatement}
