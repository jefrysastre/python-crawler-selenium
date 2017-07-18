import json
import os


class Config:
    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __setitem__(self, key, value):
        self.__dict__[key] = value


    def dump(self, path = None):
        if(path == None):
            return json.dumps(self.__dict__)
        else:
            if os.path.exists(path):
                raise Exception('File already exist!')
            with open(path, 'w') as outFile:
                json.dump(self.__dict__, outFile)

    @classmethod
    def load(cls, path):
        if os.path.exists(path):
            with open(path, 'r') as inFile:
                obj = json.load(inFile)
                return Config.__load(obj)
        else:
            raise Exception('File not found')

    @classmethod
    def __load(cls, obj):
        if type(obj) in (int, float, bool, str, unicode):
            return obj
        if(isinstance(obj, list)):
            return [Config.__load(item) for item in obj]
        result = cls()
        for prop in obj:
            if isinstance(obj[prop], dict) or isinstance(obj[prop], list):
                result[prop] = Config.__load(obj[prop])
            else:
                result[prop] = obj[prop]
        return result