class LogType:
    '''
        This class stores and exposes information about a log type.
    '''

    def __init__(self, ltInfo):
        for key in ltInfo:
            setattr(self, key, ltInfo[key])

    def getLt(self):
        return getattr(self, "id")
    
    def getFuncLt(self):
        return getattr(self, "funcid")
    
    def getType(self):
        return getattr(self, "type")

    def isFunction(self):
        return getattr(self, "type") == "function"
    
    def isUnique(self):
        return getattr(self, "isUnique")
        
    def getName(self):
        return getattr(self, "name")

