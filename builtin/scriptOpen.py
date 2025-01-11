from tage.api import api

def load(tage):
    return True

name = "open"

def scriptOpen(tage, script_location, *args, **kargs):
        """Changes script pointer to start of specified script. Accepts commands at the end of the argument"""
        api.open_script(tage, script_location)
        if len(args) != 0:
            api.execute_command(tage, '\"'+'" "'.join(args)+'\"')

def get_command():
    return {name: scriptOpen}
