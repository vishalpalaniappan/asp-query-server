import json
from decoder.Variable import Variable
from decoder.LogType import LogType

class CdlHeader:

    def __init__(self, headerJsonString):
        self.ltMap = {}
        self.varMap = {}
        self.saveHeaderInformation(headerJsonString)

    def saveHeaderInformation(self, headerJsonString):
        '''
            Save the header information while creating
            objects to store the variable and logtype
            information.
        '''
        header = json.loads(headerJsonString)

        self.fileTree = header["fileTree"]
        self.metadata = header["metadata"]
        self.sysinfo = header["sysinfo"]

        for lt in header["ltMap"]:
            self.ltMap[int(lt)] = LogType(header["ltMap"][lt])
        
        for lt in header["varMap"]:
            self.varMap[int(lt)] = Variable(header["varMap"][lt])


    def getLtInfo(self, logtype):
        '''
            Returns logtype info given a logtype id.
        '''
        return self.ltMap[logtype]
    
    def getVarInfo(self, varType):
        '''
            Returns variable info given a variable type.
        '''
        return self.varMap[varType]
    
    def getFileFromLt(self, lt):
        '''
            Returns the file that this logtype belongs to
        '''
        for file in self.fileTree:
            lt_value = int(lt)
            minLt = self.fileTree[file]["minLt"]
            maxLt = self.fileTree[file]["maxLt"]
            if (lt_value >= minLt and lt_value < maxLt):
                return file
            
        return None
    
    def getMetadata(self):
        '''
            Returns the metadata for the current program.
        '''
        return self.metadata
    
    def getSysInfo(self):
        '''
            Returns the system information.
        '''
        return self.sysinfo
    


