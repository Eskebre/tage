def load(tage):
    return True

name = "goto"

def goto(tage, label: str, *args) -> None:
        """Sets pointer to label position"""
        tage.pointer = tage.labels[tage.script_pointer][label.lower().strip()]

def get_command():
    return {name: goto}
