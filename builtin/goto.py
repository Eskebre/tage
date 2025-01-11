from tage.api import api

def load(tage):
    return True

name = "goto"

def goto(tage, label: str, *args, **kargs) -> None:
        api.goto_label(tage, label)

def get_command():
    return {name: goto}
