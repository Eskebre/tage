from time import sleep


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
            "print": self.printMessage,
            "pause": self.pause,
            "goto": self.goto,
            "call": self.call,
            "return": self.returnToStack,
            "option": self.option,
            "choice": self.choice,
            "clear": self.clearList,
            "set": self.setVariable,
            "input": self.user_input,
            "if": self.ifStatement,
            "wait": self.wait,
            "load": self.scriptLoad,
            "unload": self.scriptUnload,
            "open": self.scriptOpen,
            "write": self.writeToFile
        }
    
    def scriptLoad(self, script_location:str, *args) -> None:
        """Loads and cleans script file to scripts dictonary"""
        with open(self.script_folder+script_location) as f:
            script = f.readlines()
        self.scripts[script_location] = []
        # Removes comments and empty lines
        for i in script:
            if not (i.strip().startswith("#") or i.strip() == ""):
                self.scripts[script_location].append(i)
        self.findLabels(script_location)

    def scriptUnload(self, script_location, *args) -> None:
        """Removes script from scripts dictonary"""
        try:
            self.scripts.pop(script_location)
        except KeyError:
            pass

    def scriptOpen(self, script_location, *args):
        """Changes script pointer to start of specified script. Accepts commands at the end of the argument"""
        self.pointer = 0
        self.script_pointer = script_location
        if len(args) != 0:
            self.executeCommand('\"'+'" "'.join(args)+'\"')
        

    def writeToFile(self,file_name,data,write_mode="a", *args):
        """Writes a line of data to a file, supports changeing write mode"""
        with open(self.data_folder+file_name,write_mode) as f:
            f.write(data)

    def findLabels(self, script_location):
        """Finds all labels within a script and stores it to labels list"""
        for i, command in enumerate(self.scripts[script_location], 0):
            if command.strip().startswith(":"):
                self.labels.setdefault(script_location, {}) #Creates a dictionary key if not exists
                self.labels[script_location][command.strip(" :\n").lower()] = i

    def pause(self, *args) -> None:
        """Waits for user to return"""
        input()

    def wait(self, time, *args) -> None:
        """Waits the specified time in miliseconds"""
        sleep(int(time)/1000)

    def user_input(self, name, *args) -> None:
        """Gets user input and puts it into a variable"""
        self.variables[name] = input().replace("\"", "&quote&")

    def goto(self, label: str, *args) -> None:
        """Sets pointer to label position"""
        self.pointer = self.labels[self.script_pointer][label.lower().strip()]

    def call(self, label: str, *args) -> None:
        """Saves pointer position to stack then goes to label position"""
        self.stack.append([self.current_script_pointer, self.current_pointer])
        self.goto(label)

    def returnToStack(self) -> None:
        """Sets pointer to the top of the pointer stack and removes the stack item. Ignored it nothing is on the stack"""
        if len(self.stack) == 0:
            return
        self.script_pointer = self.stack[-1][0]
        self.pointer = self.stack[-1][1]
        self.stack.pop()

    def ifStatement(self, value1, op, value2, *args) -> None:
        """Executes a command if operation is true"""
        if self.comparativeOperation(value1, op, value2):
            self.executeCommand('\"'+'" "'.join(args)+'\"')
        return

    def option(self, selector: str, *args) -> None:
        """Adds the selector and command to options list"""
        #The string concatination stuff is to encase each argument with quation marks for later
        self.option_list[selector] = '"' + '" "'.join(args) + '"'

    def choice(self, case_sensitive=0, *args) -> None:
        """Allows user input to select an option and run the coresponding command.
           If require option is 1 it will repeat user input until a correct option is selected"""
        while True:
            user_input = input()
            for i in self.option_list.keys():
                if int(case_sensitive) and user_input == i:
                    self.executeCommand(self.option_list[i])
                    return
                elif not int(case_sensitive) and user_input.lower() == i.lower():
                    self.executeCommand(self.option_list[i])
                    return
                #If option has this value, it will always run when iterated over. Note this option should be put at the bottom of the list
                elif i == "*":              
                    self.executeCommand(self.option_list[i])
                    return

    def clearList(self, list_to_clear, *args) -> None:
        """Clears specified list/dict"""
        if list_to_clear == "option":
            self.option_list.clear()
        elif list_to_clear == "stack":
            self.stack.clear()

    def setVariable(self, name, *args):
        """Puts the variable into the variables dict"""
        self.variables[name] = self.variableOperation("".join(args))

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

    def step(self) -> bool:
        """Handle a single iteration"""

        #Stores the current pointer location to prevent issues when going across files
        self.current_pointer = self.pointer
        self.current_script_pointer = self.script_pointer
        try:
            #Gets the command from the script to be executed
            self.executeCommand(self.scripts[self.script_pointer][self.pointer])
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
        self.command_map[arguments[0]](*arguments[1:])                  #Runs function from command map

    def splitArguments(self, command: str) -> list[str]:
        """Splits command into list of arguments"""
        output = []
        # If no quotation marks split using space char
        if command.count("\"") == 0:
            return command.strip().split(" ")

        # Throw error if an odd number of quotation marks are in the command
        elif command.count("\"") % 2 == 1:
            raise TageOpenString

        # Splits string from quotation marks then splits on space outside of quotation marks
        string_split: str = command.split("\"")
        for i in range(len(string_split)):
            if i % 2 == 0:
                output += string_split[i].strip().replace("&quote&","\"").split(" ")
            else:
                output.append(string_split[i].replace("&quote&", "\""))

        # Removes empty strings
        for i in output:
            if i.strip() == "":
                output.remove(i)
        return output

    def variableParser(self, command: str) -> str:
        """Inserts variables into commands"""
        #Checks if the rest of the function should be run or something is not as expected
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
        return output.encode("utf_8", 'ignore').decode('unicode_escape') #The encoding and decoding is to allow escape codes to work

    
    def variableOperation(self, input:str, *args) -> str:
        """Takes a string input and performs basic mathmatical operations if it only contains numbers and operators"""
        # List of mathmatical operators
        operator_list = "+-*/^" 
        pre_split_string = input.replace(",", "").replace(" ", "")
        
        for i in operator_list:
            if i != "-":
                pre_split_string = pre_split_string.replace(i, f",{i},")
            else:
                # Replace minus with an addition and set next number negative
                pre_split_string = pre_split_string.replace(i, f",+,-") 
        tokens = pre_split_string.split(",")
        
        #Check if any not related characters are in the string
        for i in tokens:
            if not str(i) in operator_list and not self.isDigit(i):
                return input
        
        
        output = 0
        operator = "+" 
        for i in tokens:
            #Replace empty strings with zero
            num = 0 if i == "" else i
            if str(i) in operator_list:
                operator = i
                continue
            #The place where the math stuff happens
            num = int(num)
            if operator == "+":
                output += num
            elif operator == "*":
                output *= num
            elif operator == "/":
                output /= num
            elif operator == "^":
                output = pow(output,num)
        return str(output)

    def comparativeOperation(self, value1, op, value2, *args) -> bool:
        """Checks if values are equal based on an operator. Less and greater than only work on numbers."""
        operator_list = ["=","==","!=","<",">","<=",">="]
        if op not in operator_list:
            raise TageInvalidOperator
        
        #Numeric and string comparisons
        if "!" in op:
            if value1 != value2:
                return True
        elif "=" in op:
            if value1 == value2:
                return True
        
        #Numeric comparisons
        if self.isDigit(value1) and self.isDigit(value2):
            if "<" in op:
                if value1 < value2:
                    return True
            if ">" in op:
                if value1 > value2:
                    return True
        return False
        
        
    

    @staticmethod
    def isDigit(input):
        """Checks if the input can be converted to an int"""
        try:
            int(input)
        except ValueError:
            return False
        else:
            return True
        

class TageOpenString(Exception):
    """Thrown in the condition of a string having no closing quotation marks"""
    pass


class TageOpenVariable(Exception):
    """Thrown in the condition of a variable having no closing andpersand"""
    pass

class TageInvalidOperator(Exception):
    """Thrown in the case of a operator is not valid"""
    pass