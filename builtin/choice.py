def load():
    pass

name = "choice"

def choice(self, case_sensitive=0, *args) -> None:
    """Allows user input to select an option and run the coresponding command.
       If require option is 1 it will repeat user input until a correct option is selected"""
    while True:
        user_input = input()
        for i in self.option_list.keys():
            if int(case_sensitive) and user_input == i:
                self.executeCommand(self.option_list[i])
                return
            elif not int(case_sensitive) and user_input.lower() == i.lower():
                self.executeCommand(self.option_list[i])
                return
            #If option has this value, it will always run when iterated over. Note this option should be put at the bottom of the list
            elif i == "*":              
                self.executeCommand(self.option_list[i])
                return
def get_command():
    return name, choice
