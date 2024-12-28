def load(tage):
    return True

name = "write"

def writeToFile(tage,file_name,data,write_mode="a", *args):
        """Writes a line of data to a file, supports changeing write mode"""
        with open(tage.data_folder+file_name,write_mode) as f:
            f.write(data)

def get_command():
    return name, writeToFile
