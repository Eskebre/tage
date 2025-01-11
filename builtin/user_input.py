from tage.api import api

def load(tage):
    return True

name = "input"

def user_input(tage, name, *args, **kargs) -> None:
        """Gets user input and puts it into a variable"""
        api.set_variable(name, input().replace("\"", "&quote&").strip())

def get_command():
    return {name: user_input}
