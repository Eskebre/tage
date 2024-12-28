def load(tage):
    return True

name = "call"

def call(tage, label: str, *args) -> None:
        """Saves pointer position to stack then goes to label position"""
        tage.stack.append([tage.current_script_pointer, tage.current_pointer])
        tage.executeCommand(f'goto {label}')

def get_command():
    return name, call
