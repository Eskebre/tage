from tage.api import api

def load(tage):
    return True

name = "choice"

def choice(tage, case_sensitive=0, *args, **kargs) -> None:
    """Allows user input to select an option and run the coresponding command.
       If require option is 1 it will repeat user input until a correct option is selected"""
    while True:
        user_input = input().strip()
        options = api.get_options(tage)
        # Checks if user input matches an option
        for i in options.keys():
            if int(case_sensitive) and user_input == i:  # If case sensitive
                api.execute_command(tage, options[i])
                return
            # If not case sensitive
            elif not int(case_sensitive) and user_input.lower() == i.lower():
                api.execute_command(tage, options[i])
                return
            # If option has this value, it will act as a wild card and always run when iterated over.
            # Note this option should be put at the bottom of the option list as it ingores all options below it
            elif i == "*":
                api.execute_command(tage, options[i])
                return
                
def get_command():
    return {name: choice}
