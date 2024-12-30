def load(tage):
    return True

name = "open"

def scriptOpen(tage, script_location, *args):
        """Changes script pointer to start of specified script. Accepts commands at the end of the argument"""
        tage.pointer = 0
        tage.script_pointer = script_location
        if len(args) != 0:
            tage.executeCommand('\"'+'" "'.join(args)+'\"')

def get_command():
    return {name: scriptOpen}
