def load(tage):
    return True

name = "pause"

def pause(*args, **kargs):
    """Waits for user to return"""
    input()

def get_command():
    return {name: pause}