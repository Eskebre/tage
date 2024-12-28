def load(tage):
    return True

name = "set"

def setVariable(tage, name, *args):
    """Puts the variable into the variables dict"""
    tage.variables[name] = tage.variableOperation("".join(args))
    
def get_command():
    return name, setVariable
