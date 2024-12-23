from time import sleep

def load():
    pass

name = "wait"

def wait(self, time, *args) -> None:
        """Waits the specified time in miliseconds"""
        sleep(int(time)/1000)

def get_command():
    return name, wait