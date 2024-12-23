def load():
    pass

name = "choice"

def choice(self, case_sensitive=0, *args) -> None:
    """Allows user input to select an option and run the coresponding command.
       If require option is 1 it will repeat user input until a correct option is selected"""
    while True:
        user_input = input().strip()
        # Checks if user input matches an option
        for i in self.option_list.keys():
            if int(case_sensitive) and user_input == i:  # If case sensitive
                self.executeCommand(self.option_list[i])
                return
            # If not case sensitive
            elif not int(case_sensitive) and user_input.lower() == i.lower():
                self.executeCommand(self.option_list[i])
                return
            # If option has this value, it will act as a wild card and always run when iterated over.
            # Note this option should be put at the bottom of the option list as it ingores all options below it
            elif i == "*":
                self.executeCommand(self.option_list[i])
                return
                
def get_command():
    return name, choice
