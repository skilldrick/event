class Config:
    _eventsDir = 'events'
    
    def __init__(self):
        pass

    def eventsDir(self):
        return self._eventsDir

    def setEvent(self, event):
        self._event = event

    def getEvent(self):
        return self._event
