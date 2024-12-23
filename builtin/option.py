def load():
    pass

name = "option"

def option(self, selector: str, *args) -> None:
    """Adds the selector and command to options list"""
    #The string concatination stuff is to encase each argument with quation marks for later
    self.option_list[selector] = '"' + '" "'.join(args) + '"'

def get_command():
    return name, option
