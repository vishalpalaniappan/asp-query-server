
class UniqueTrace:

    def __init__(self):
        self.traceEvents = []

    def addEvents(self, events):
        for event in events:
            self.traceEvents.append(event)

    def getNumberOfTraceEvents(self):
        return len(self.traceEvents)