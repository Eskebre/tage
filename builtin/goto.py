def load():
    pass

name = "goto"

def goto(self, label: str, *args) -> None:
        """Sets pointer to label position"""
        self.pointer = self.labels[self.script_pointer][label.lower().strip()]

def get_command():
    return name, goto
