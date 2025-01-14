class api:
    @staticmethod
    def execute_command(tage, command):
        tage.executeCommand(command)

    @staticmethod
    def push_pointer_to_stack(tage):
        tage.stack.append([tage.current_script_pointer, tage.current_pointer])

    @staticmethod
    def pop_stack_to_pointer(tage):
        """Sets pointer to the top of the pointer stack and removes the stack item. Ignored if nothing is on the stack"""
        if len(tage.stack) == 0:
            return
        # Update pointers to last item of the stack
        tage.script_pointer = tage.stack[-1][0]
        tage.pointer = tage.stack[-1][1]
        tage.stack.pop()

    @staticmethod
    def open_script(tage, location):
        tage.skip_pointer = True
        tage.pointer = 0
        tage.script_pointer = location

    @staticmethod
    def goto_label(tage, label):
        """Sets pointer to label position"""
        tage.skip_pointer = True
        tage.pointer = tage.labels[tage.script_pointer][label.lower().strip()]

    @staticmethod
    def get_options(tage) -> dict:
        return tage.option_list
    
    @staticmethod
    def set_option(tage, selector: str, *args):
        #The string concatination stuff is to encase each argument with quation marks for later
        tage.option_list[selector] = '"' + '" "'.join(args) + '"'
    
    @staticmethod
    def set_variable(tage, name, value, try_operation=True):
        """Puts the variable into the variables dict"""
        #value = value
        try:
            value = "".join(value)
        except TypeError:
            value = str(value)

        if try_operation:
            value = tage.variableOperation(value)
        tage.variables[name] = value

    @staticmethod
    def get_variable(tage, name):
        return tage.variables.get(name, False)