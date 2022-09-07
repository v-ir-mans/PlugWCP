import json
import os

#Gets path off settings file by getting path of itself, removing all after "app" and adding settings file name
parent_dir=os.path.realpath(__file__).split("app")[0]
config_path=parent_dir+"settings.config.json"


class config:
    def __init__(self):
        self.path=config_path
        self.load()
    def load(self):
        with open(self.path,"r") as f:
            self.data=json.load(f)
            self.mod_time=_getModTime_(self.path)
    def update(self):
        with open(self.path,"w") as f:
            return json.dump(self.data,f)
    def hasChanged(self):
        if self.mod_time!=_getModTime_(self.path):
            with open(self.path,"r") as f:
                if self.data!=json.load(f):
                    return True
        return False

def _getModTime_(path):
    return os.path.getmtime(path)

def _compareDict_():
    pass
