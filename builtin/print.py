from time import sleep
def load(tage):
    return True

name = "print"

def printMessage(tage, message: str, delay: int = 0, new_line=1, *args) -> None:
    """Wrapper for the print function, Delay specifies the amount of time between each character being printed"""
    escape_code_chars = "\003\x1b[;0123456789:]"  # List of esacape code chars to ignore for delay print
    # This basically makes escape codes works
    message = message.encode("utf_8", 'ignore').decode('unicode_escape')
    int(new_line)
    escape_code = False
    if delay == 0:  # If no delay, print message as normal
        print(message, end="")
        if int(new_line):  # Wether to print a new line
            print("")
        return
    for i in message:  # Prints message on delay
        print(i, end="", flush=True )
        # Used to ignore ansi escape codes for delay print
        if i == "\003" or i == "\x1b":  
            escape_code = True
        if escape_code:
            if i not in escape_code_chars:
                escape_code = False
        else:
            sleep(int(delay)/1000)
    if int(new_line):  # Wether to print a new line
        print("")

def get_command():
    return name, printMessage