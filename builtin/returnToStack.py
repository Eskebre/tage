def load(tage):
    return True

name = "return"

def returnToStack(tage) -> None:
        """Sets pointer to the top of the pointer stack and removes the stack item. Ignored if nothing is on the stack"""
        if len(tage.stack) == 0:
            return
        # Update pointers to last item of the stack
        tage.script_pointer = tage.stack[-1][0]
        tage.pointer = tage.stack[-1][1]
        tage.stack.pop()

def get_command():
    return name, returnToStack
