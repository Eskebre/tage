from time import sleep

def load(tage):
    return True

name = "wait"

def wait(tage, time, *args) -> None:
        """Waits the specified time in miliseconds"""
        sleep(int(time)/1000)

def get_command():
    return {name: wait}