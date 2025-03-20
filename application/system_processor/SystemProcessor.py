import os
from decoder.Cdl import Cdl
from UniqueTrace import UniqueTrace

class SystemProcessor:

    def __init__(self, logFolder):
        '''
            Initialize the system processor with the logs
            from the given folder.
        '''
        self.logFolder = logFolder
        self.logFiles = []
        self.traceEvents = {}

        self.parseSystemLogFiles()

    def parseSystemLogFiles(self):
        '''
            Parse the system log files contained in folder.
        '''
        files = os.listdir(self.logFolder)

        for file in files:
            _path = os.path.join(self.logFolder, file)
            cdlFile = Cdl(_path)
            self.addTraceEvents(cdlFile.traceEvents)

            self.logFiles.append(cdlFile)

    def addTraceEvents(self, traceEvents):
        '''
            Add trace events from log files to system processor list.
        '''
        for traceUid in traceEvents:            
            if traceUid not in self.traceEvents:
                self.traceEvents[traceUid] = UniqueTrace()

            self.traceEvents[traceUid].addEvents(traceEvents[traceUid])


if __name__ == "__main__":
    SYSTEM_LOG_FILES = "../sample_system_logs/"
    processor = SystemProcessor(SYSTEM_LOG_FILES)