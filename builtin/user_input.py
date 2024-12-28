def load(tage):
    return True

name = "input"

def user_input(tage, name, *args) -> None:
        """Gets user input and puts it into a variable"""
        tage.variables[name] = input().replace("\"", "&quote&").strip()

def get_command():
    return name, user_input
