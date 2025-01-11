from tage.api import api

def load(tage):
    return True

name = "call"

def call(tage, label: str, *args, **kargs) -> None:
        """Saves pointer position to stack then goes to label position"""
        api.push_pointer_to_stack(tage)
        api.execute_command(tage, f"goto {label}")

def get_command():
    return {name: call}
