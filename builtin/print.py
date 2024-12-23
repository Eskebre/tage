from time import sleep
def load():
    pass

name = "print"

def printMessage(self, message: str, delay: float = 0, new_line=True, *args) -> None:
    """Wrapper for the print function, Delay specifies the amount of time between each character being printed"""

    escape_code_chars = "\003\x1b[;0123456789:]"
    message = message.encode("utf_8", 'ignore').decode('unicode_escape')
    int(new_line)
    escape_code = False
    if delay == 0:                  #If no delay, print message as normal
        print(message, end="")
        return
    for i in message:               #Prints message on delay
        print(i, end="", flush=True)
        if i == "\003" or i == "\x1b":             #Used to ignore ansi escape codes for delay
            escape_code = True
        if escape_code:
            if i not in escape_code_chars:
                escape_code = False
        else:
            sleep(int(delay)/1000)
    if int(new_line):               #Wether to print a new line
        print("")

def get_command():
    return name, printMessage