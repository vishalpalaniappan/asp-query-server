from pathlib import Path
from clp_ffi_py.ir import ClpIrFileReader
from application.system_processor.decoder.CDL_CONSTANTS import LINE_TYPE
from application.system_processor.decoder.CdlLogLine import CdlLogLine
from application.system_processor.decoder.CdlHeader import CdlHeader

import os

class CdlDecoder:

    def __init__(self, filePath):
        '''
            Initialize the CDL reader.
        '''
        self.logFileName = os.path.basename(filePath)
        self.filePath = filePath
        self.header = None  

        self.execution = []
        self.exception = None
        self.uniqueTraceEvents = {}
        self.callStack = []
        self.callStacks = {}

        self.loadAndParseFile(filePath)

    def loadAndParseFile(self, filePath):
        '''
            Load and parse the file line by line.
        '''
        with ClpIrFileReader(Path(filePath)) as clp_reader:
            self.position = 0
            for log_event in clp_reader:
                self.parseLogLine(log_event)

    def parseLogLine(self, log_event):
        '''
            Parse the log line and save the relevant data.
        '''
        currLog = CdlLogLine(log_event)

        if currLog.type == LINE_TYPE["IR_HEADER"]:
            self.header = CdlHeader(currLog.value)
        elif currLog.type == LINE_TYPE["EXCEPTION"]:
            self.exception = currLog.value
        elif currLog.type == LINE_TYPE["EXECUTION"]:
            self.lastExecution = self.position
            self.execution.append(currLog)
            self.addToCallStack(currLog)
            self.position += 1
        elif currLog.type == LINE_TYPE["VARIABLE"]:
            self.execution.append(currLog)
            self.saveUniqueId(currLog)
            self.position += 1

    def saveUniqueId(self, variable):
        '''
            Save the asp_uid variable value to the top of the stack.
        '''
        varInfo = self.header.getVarInfo(variable.varId)

        if varInfo.getName() == "asp_uid":
            self.callStack[-1]["uid"] = variable.value

    def addUniqueTrace(self, uid, startPos, endPos):
        '''
            Given a start and end position of a unique trace, 
            add the position and level of each function in the
            trace to the unique trace object.
        '''

        # Add every visited function and its level in the stack to the trace list 
        trace = []
        for position in range(startPos, endPos):
            lineType = self.execution[position]

            if lineType.type == LINE_TYPE["EXECUTION"]:
                ltInfo = self.header.getLtInfo(lineType.ltId)

                if (ltInfo.isFunction()):
                    trace.append({
                        "position": position,
                        "level": len(self.callStacks[position]),
                        "name": ltInfo.getName(),
                        "lineNo": ltInfo.lineno,
                        "file": self.header.getFileFromLt(ltInfo.id)
                    })

        # Add trace to the unique traceEvents list.
        if uid not in self.uniqueTraceEvents:
            self.uniqueTraceEvents[uid] = []        
        
        self.uniqueTraceEvents[uid].append({
            "logFileName": self.logFileName,
            "trace": trace,
            "timestamp": self.execution[startPos].timestamp
        })

    def addToCallStack(self, log):
        '''
            Add the current execution to the call stack.

            - If the log is a function, add it to stack.
            - Move down stack until parent function of current log is found
            - Map the stack positions to find the log which called the function
            - Add current position to stack
            - Copy stack into global list            

            - If a unique trace function is added to stack, it is the start of a unique trace.
            - If a unique trace function is removed from stack, it is the end of a unique trace.
            - When a unique trace ends, save it to the unique trace list.
        '''
        position = len(self.execution) - 1
        ltInfo = self.header.getLtInfo(log.ltId)
        cs = self.callStack

        if (ltInfo.isFunction()):
            self.callStack.append({"position":position,"isUnique":ltInfo.isUnique})

        while (len(cs) > 0):
            currStackFuncLt = self.execution[cs[-1]["position"]].ltId
            if (int(currStackFuncLt) == int(ltInfo.getFuncLt())):
                break

            popped = cs.pop()

            # If the removed call is the end of a unique trace, then add it to the trace list.
            if popped["isUnique"]:
                self.addUniqueTrace(popped["uid"], popped["position"], position)
                
        # Update the call stack to indicate where the functions were called from.
        csFromCallPosition = []
        for cs in self.callStack:
            csFromCallPosition.append(self.getPreviousExecutionPosition(cs["position"]))
        csFromCallPosition.append(position)

        self.callStacks[position] = csFromCallPosition
    
    def getPreviousExecutionPosition(self, position):
        '''
            This function returns the previous execution position. 
            For example, when adding to the call stack, this will
            allow us to find the place where a function was called from.
        '''
        while (position >= 1):
            position -= 1
            if self.execution[position].type == LINE_TYPE["EXECUTION"]:
                return position
        return None
    

    def getNextExecutionPosition(self, position):
        '''
            This function returns the next execution position. 
        '''
        position += 1
        while (position < len(self.execution)):
            if self.execution[position].type == LINE_TYPE["EXECUTION"]:
                return position
            position += 1
        return None
    
    def getCallStackAtPosition(self, position):
        '''
            Get call stack info for the given position.
        '''
        csInfo = []
        for cs in self.callStacks[position]:
            lt = self.execution[cs].ltId
            ltInfo = self.header.getLtInfo(lt)
            funcLt = ltInfo.getFuncLt()

            if (funcLt == 0):
                funcName = "<module>"
            else:
                funcName = self.header.getLtInfo(funcLt).getName()

            csInfo.append({
                "functionName": funcName,
                "fileName": self.logFileName,
                "position": cs,
                "lineNumber": ltInfo.getLineNo()
            })

        return csInfo
    
    def getVariablesAtPosition(self, position):
        '''
            Given a position, this function returns the variables 
            that are in the current and global scope.
        '''
        pass

