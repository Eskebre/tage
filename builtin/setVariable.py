from tage.api import api

def load(tage):
    return True

name = "set"

def setVariable(tage, name, *args, **kargs):
    math = not kargs.get("m", False)
    api.set_variable(tage, name, args, math)
    
def get_command():
    return {name: setVariable}
