def load():
    pass

name = "clear"

def clearList(self, list_to_clear, *args) -> None:
    """Clears specified list/dict"""
    if list_to_clear == "option":
        self.option_list.clear()
    elif list_to_clear == "stack":
        self.stack.clear()

def get_command():
    return name, clearList
