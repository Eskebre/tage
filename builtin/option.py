from tage.api import api

def load(tage):
    return True

name = "option"

def option(tage, selector: str, *args, **kargs) -> None:
    """Adds the selector and command to options list"""
    api.set_option(tage, selector, *args)

def get_command():
    return {name: option}
