def load():
    pass

name = "call"

def call(self, label: str, *args) -> None:
        """Saves pointer position to stack then goes to label position"""
        self.stack.append([self.current_script_pointer, self.current_pointer])
        self.executeCommand(f'goto {label}')

def get_command():
    return name, call
