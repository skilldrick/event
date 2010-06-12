import unittest

from featurebroker import *
from config import Config
from filesystem import Filesystem
from mocks import MockFilesystem



class EventError(IOError):
    pass


class EventList:
    filesystem = RequiredFeature('Filesystem')
    config = RequiredFeature('Config')
    
    def __init__(self):
        self.eventsDir = self.config.eventsDir()
        self.loadEvents()

    def loadEvents(self):
        self.events = []
        dirs = self.filesystem.listToplevelDirs(self.eventsDir)
        for directory in dirs:
            self.events.append(directory)
        self.events.sort()

    def numberOfEvents(self):
        self.loadEvents()
        return len(self.events)

    def getEvents(self):
        self.loadEvents()
        return self.events

    def addEvent(self, event):
        try:
            self.filesystem.makeDir([self.eventsDir, event])
        except IOError:
            raise EventError

    def removeEvent(self, event):
        try:
            self.filesystem.removeDir([self.eventsDir, event])
        except OSError:
            raise EventError
        
            
class EventListTests(unittest.TestCase):
    def setUp(self):
        self.eventList = EventList()

    def testAddEvent(self):
        self.eventList.addEvent('bob')

        
def suite():
    features.provide('Filesystem', MockFilesystem)
    features.provide('Config', Config)
    testSuite = unittest.makeSuite(EventListTests)
    return testSuite

    
def main():
    unittest.TextTestRunner().run(suite())

if __name__ == '__main__':
    main()
