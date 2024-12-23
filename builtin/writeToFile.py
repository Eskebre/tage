def load():
    pass

name = "write"

def writeToFile(self,file_name,data,write_mode="a", *args):
        """Writes a line of data to a file, supports changeing write mode"""
        with open(self.data_folder+file_name,write_mode) as f:
            f.write(data)

def get_command():
    return name, writeToFile
