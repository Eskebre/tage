def load(tage):
    return True

name = "nop"

def nop(tage, *args, **kargs) -> None:
        """No operation"""
        return

def get_command():
    return {name: nop}
