from tage.api import api

def load(tage):
    return True

name = "set"

def setVariable(tage, name, *args, **kargs):
    api.set_variable(tage, name, args)
    
def get_command():
    return {name: setVariable}
