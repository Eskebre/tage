def load():
    pass

name = "return"

def returnToStack(self) -> None:
        """Sets pointer to the top of the pointer stack and removes the stack item. Ignored it nothing is on the stack"""
        if len(self.stack) == 0:
            return
        self.script_pointer = self.stack[-1][0]
        self.pointer = self.stack[-1][1]
        self.stack.pop()

def get_command():
    return name, returnToStack
