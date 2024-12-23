def load():
    pass

name = "open"

def scriptOpen(self, script_location, *args):
        """Changes script pointer to start of specified script. Accepts commands at the end of the argument"""
        self.pointer = 0
        self.script_pointer = script_location
        if len(args) != 0:
            self.executeCommand('\"'+'" "'.join(args)+'\"')

def get_command():
    return name, scriptOpen
