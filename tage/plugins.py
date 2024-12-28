import os
from importlib import util

class Plugin():

    def __init__(self):
        self.plugin_modules = []
        pass

    def load_plugins(self, folder):
        self.plugin_modules = []
        
        for plugin in self.get_plugin_files(folder):
            self.plugin_modules.append(load_module(os.path.join(folder,plugin)))
        
    def get_plugin_files(self, folder):
        files = os.listdir(folder)
        plugin_files = []
        for file in files:
            if os.path.isfile(os.path.join(folder,file)):
                if file.endswith(".py"):
                    plugin_files.append(file)
        return plugin_files

    def get_plugins(self):
        return self.plugin_modules

def load_module(path):
    name = os.path.split(path)[-1]
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module