import unittest

from featurebroker import *
from config import Config
from filesystem import Filesystem


class AddEventError(IOError):
    pass


class EventList:
    """
    This class will contain event handling methods currently handled
    by gui and filesystem
    """

    filesystem = RequiredFeature('Filesystem')
    config = RequiredFeature('Config')
    events = []
    
    def __init__(self):
        self.eventsDir = self.config.eventsDir()
        dirs = self.filesystem.listDirs(self.eventsDir)
        numberOfDirs = len(dirs)
        if numberOfDirs == 0:
            self.noEvents = True
        else:
            self.noEvents = False
        self.loadEvents()

    def loadEvents(self):
        dirs = self.filesystem.listDirs(self.eventsDir)
        for directory in dirs:
            self.events.append(directory)

    def addEvent(self, event):
        try:
            self.filesystem.makeDir([self.eventsDir, event])
        except IOError:
            raise AddEventError
        
            
class MockFilesystem (Filesystem):
    def listDirs(self, root):
        return ['My event', 'event2', 'another event']

    def makeDir(self, dirname):
        if not self.checkValidDir(dirname):
            raise IOError
        if not type(dirname) == list:
            assert False, 'dirname should be list'


class EventListTests(unittest.TestCase):
    def setUp(self):
        self.eventList = EventList()

    def testNoEvents(self):
        self.assertFalse(self.eventList.noEvents)

    def testAddEvent(self):
        self.eventList.addEvent('bob')
        

def main():
    features.provide('Filesystem', MockFilesystem)
    features.provide('Config', Config)
    unittest.main()

if __name__ == '__main__':
    main()
