from time import sleep
from importlib import util
from .plugins import Plugin

class Tage:

    def __init__(self) -> None:
        # Stores all lines of the file loaded into it
        self.scripts = {'file': []}
        # Contains dict of all labels and their line number
        self.labels = {"file": {}}
        self.variables = {
            "": "&",  # Double && will return &
            "\"": "&quote&",  # Gets replaced with a quotation mark
            "true": "1",
            "false": "0",
            "ansi": "\033[",
            "color": "\033[38;5;",
            "backcolor": "\033[48;5;",
            "reset_color": "\033[0m"
        }
        self.option_list = {}
        self.pointer = 0
        self.current_script_pointer = 0
        self.script_pointer = ""
        self.current_script_pointer = ""
        self.stack = []  # Stores previous file and pointer location when using call and can be returned to by using 'return'
        self.script_folder = "scripts/"
        self.assets_folder = "assets/"
        self.data_folder = "data/"
        self.command_map = {  # Maps commands to functions
            "load": self.scriptLoad,
            "unload": self.scriptUnload,
        }
        self.load_plugins('builtin/')
        self.load_plugins()
    
    plugins = Plugin()


    def load_plugins(self, folder='plugins/'):
        self.plugins.load_plugins(folder)
        
        for i in self.plugins.get_plugins():
            try:
                if i.load(self):
                    try:
                        command = i.get_command()
                        self.command_map.update(command)
                    except:
                        pass
            except:
                pass
            

    @staticmethod            
    def scriptLoad(self, script_location:str, *args, **kargs) -> None:
        """Loads and cleans script file to scripts dictonary"""
        with open(self.script_folder+script_location) as f:
            script = f.readlines()
        self.scripts[script_location] = []
        # Removes comments and empty lines
        for i in script:
            if not (i.strip().startswith("#") or i.strip() == ""):
                self.scripts[script_location].append(i)
        self.findLabels(script_location)
    @staticmethod
    def scriptUnload(self, script_location, *args, **kargs) -> None:
        """Removes script from scripts dictonary"""
        try:
            self.scripts.pop(script_location)
        except KeyError:
            pass
    
        

    

    def findLabels(self, script_location):
        """Finds all labels within a script and stores it to labels list"""
        for i, command in enumerate(self.scripts[script_location], 0):
            if command.strip().startswith(":"):
                self.labels.setdefault(script_location, {}) #Creates a dictionary key if not exists
                self.labels[script_location][command.strip(" :\n").lower()] = i


    def step(self) -> bool:
        """Handle a single iteration"""

        # Stores the current pointer location to prevent issues when going across files
        self.current_pointer = self.pointer
        self.current_script_pointer = self.script_pointer
        try:
            # Gets the command from the script to be executed
            self.executeCommand(
                self.scripts[self.script_pointer][self.pointer])
        # Exception handling
        except TageOpenString:
            print(
                f"\nERROR: Unclosed string in {self.script_pointer} on line {self.pointer+1}: '{self.scripts[self.script_pointer][self.pointer].strip()}'")
            return False
        except TageOpenVariable:
            print(
                f"\nERROR: Unclosed variable in {self.script_pointer} on line {self.pointer+1}: '{self.scripts[self.script_pointer][self.pointer].strip()}'")
            return False
        except ValueError as e:
            print(
                f"\nERROR: Value error in {self.script_pointer} on line {self.pointer+1}: '{self.scripts[self.script_pointer][self.pointer].strip()}'\n{e}")
            return False
        except Exception as e:
            print(
                f"\nERROR: Error in {self.script_pointer} on line {self.pointer+1}: '{self.scripts[self.script_pointer][self.pointer].strip()}'\n{e}")
            return False

        self.pointer += 1
        # If pointer has reached the end of the file
        if len(self.scripts[self.script_pointer]) <= self.pointer:
            return False
        return True

    def executeCommand(self, command: str) -> None:
        """Gets the arguments and run the function specified within the command"""
        if command.strip().startswith(':'):
            return
        arguments = self.splitArguments(self.variableParser(command))
        self.command_map[arguments[''][0]](self, *arguments[''][1:], **arguments)

    def splitArguments(self, command: str) -> dict:
        """Splits command into list of arguments"""
        output = []
        kargs = {"test":""}
        # If no quotation marks split using space char
        if command.count("\"") == 0:
            return {'':command.strip().split(" ")} | kargs

        # Throw error if an odd number of quotation marks are in the command
        elif command.count("\"") % 2 == 1:
            raise TageOpenString

        # Splits string from quotation marks then splits on space outside of quotation marks
        # Its expected that every other item in the list is a string
        # Adds in addition quotes aswell from not a string
        string_split: list[str] = command.split("\"")
        for i in range(len(string_split)):
            if i % 2 == 0:
                output += string_split[i].strip().replace("&quote&","\"").split(" ")
            else:
                output.append(string_split[i].replace("&quote&", "\""))
        for i in output:
            if i.strip() == "":
                output.remove(i)
        return {'':output} | kargs

    def variableParser(self, command: str) -> str:
        """Inserts variables into commands"""
        # Checks if the rest of the function should be run or something is not as expected
        if command.count("&") == 0:
            return command
        elif command.count("&") % 2 == 1:
            raise TageOpenVariable

        string_split = command.split("&")
        output = ""
        # Every odd item within the list is assumed to be a variable and is replaced with the corresponding value
        for i in range(len(string_split)):
            if i % 2 == 0:
                output += string_split[i]
            else:
                if string_split[i] in self.variables:
                    output += self.variables[string_split[i]]
        # The encoding and decoding is to allow escape codes to work
        return output.encode("utf_8", 'ignore').decode('unicode_escape')

    def variableOperation(self, command: str, *args) -> str:
        """Takes a string input and performs basic mathmatical operations if it only contains numbers and operators"""
        operator_list = "+-*/^"
        pre_split_string = command.replace(",", "").replace(" ", "")

        for i in operator_list:
            if i != "-":
                pre_split_string = pre_split_string.replace(i, f",{i},")
            else:
                pre_split_string = pre_split_string.replace(i, ",+,-")
        tokens = pre_split_string.split(",")

        # Check if any not related characters are in the string
        for i in tokens:
            if not str(i) in operator_list and not self.isDigit(i):
                return command
        output = 0
        operator = "+"
        for i in tokens:
            # Replace empty strings with zero
            num = 0 if i == "" else i
            if str(i) in operator_list:
                operator = i
                continue
            # The place where the math stuff happens
            num = int(num)
            if operator == "+":
                output += num
            elif operator == "*":
                output *= num
            elif operator == "/":
                output /= num
            elif operator == "^":
                output = pow(output, num)
        return str(output)

    def comparativeOperation(self, value1, op, value2, *args) -> bool:
        """Checks if values are equal based on an operator. Less and greater than only work on numbers."""
        operator_list = ["=", "==", "!=", "<", ">", "<=", ">="]
        if op not in operator_list:
            raise TageInvalidOperator

        if "!" in op:
            if value1 != value2:
                return True
        elif "=" in op:
            if value1 == value2:
                return True

        if self.isDigit(value1) and self.isDigit(value2):
            if "<" in op:
                if value1 < value2:
                    return True
            if ">" in op:
                if value1 > value2:
                    return True
        return False

    @staticmethod
    def isDigit(num):
        """Checks if the input can be converted to an int"""
        try:
            int(num)
        except ValueError:
            return False
        else:
            return True


class TageOpenString(Exception):
    """Thrown in the condition of a string having no closing quotation marks"""


class TageOpenVariable(Exception):
    """Thrown in the condition of a variable having no closing andpersand"""


class TageInvalidOperator(Exception):
    """Thrown in the case of a operator is not valid"""
