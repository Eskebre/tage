from tage.api import api

def load(tage):
    return True

name = "return"

def returnToStack(tage, *args, **kargs) -> None:
        """Sets pointer to the top of the pointer stack and removes the stack item. Ignored if nothing is on the stack"""
        if len(tage.stack) == 0:
            return
        api.pop_stack_to_pointer(tage)

def get_command():
    return {name: returnToStack}
