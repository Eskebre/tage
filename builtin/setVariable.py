def load():
    pass

name = "set"

def setVariable(self, name, *args):
    """Puts the variable into the variables dict"""
    self.variables[name] = self.variableOperation("".join(args))
    
def get_command():
    return name, setVariable
