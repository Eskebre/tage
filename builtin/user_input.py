def load():
    pass

name = "input"

def user_input(self, name, *args) -> None:
        """Gets user input and puts it into a variable"""
        self.variables[name] = input().replace("\"", "&quote&")

def get_command():
    return name, user_input
