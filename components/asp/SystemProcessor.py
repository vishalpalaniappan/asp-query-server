import os
from Cdl import Cdl
import json
from pathlib import Path
from database.TableWriter import TableWriter

class SystemProcessor:

    def __init__(self, logFolder):
        '''
            Initialize the system processor with the logs from the given folder.
        '''
        self.logFolder = logFolder
        self.logFiles = []
        self.uniqueTraces = {}
        self.database = TableWriter()

        self.parseSystemLogFiles()

    def parseSystemLogFiles(self):
        '''
            Parse the system log files contained in folder.
        '''
        files = os.listdir(self.logFolder)

        for logFileName in files:
            if logFileName.endswith(".clp.zst"):
                cdlFile = Cdl(os.path.join(self.logFolder, logFileName))
                self.addUniqueTraceEvents(cdlFile)
                self.database.write_file(cdlFile)
                self.logFiles.append(cdlFile)
        
        # Sort the trace events by timestamp
        for uid in self.uniqueTraces:
            self.uniqueTraces[uid].sort(key=lambda x: x["startTs"], reverse=False)

        # Save trace events to json file
        with open("traceEvents.json", "w+") as f:
            f.write(json.dumps(self.uniqueTraces))

    def addUniqueTraceEvents(self, cdlFile):
        '''
            Add trace events from log files to system unique trace list.
        '''
        traceEvents = cdlFile.getUniqueTraceEvents()
        for traceUid in traceEvents:            
            if traceUid not in self.uniqueTraces:
                self.uniqueTraces[traceUid] = []

            self.uniqueTraces[traceUid] += traceEvents[traceUid]

    def getFileTrees(self):
        '''
            Returns the file tree for all programs in the system
        '''
        fileTrees = {}
        for log in self.logFiles:
            fileTrees[log.logFileName] = log.getFileTree()

        return fileTrees

if __name__ == "__main__":
    rootDir = Path(__file__).resolve().parents[0]
    SYSTEM_LOG_FILES = rootDir / "sample_system_logs"
    processor = SystemProcessor(SYSTEM_LOG_FILES)