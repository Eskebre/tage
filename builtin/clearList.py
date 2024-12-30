def load(tage):
    return True

name = "clear"

def clearList(tage, list_to_clear, *args) -> None:
    """Clears specified list/dict"""
    if list_to_clear == "option":
        tage.option_list.clear()
    elif list_to_clear == "stack":
        tage.stack.clear()

def get_command():
    return {name: clearList}
