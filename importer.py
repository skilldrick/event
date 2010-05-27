import unittest

from filesystem import Filesystem
from featurebroker import *

class Importer:
    filesystem = RequiredFeature('Filesystem')
    
    def __init__(self):
        pass

    def setLocations(self, source, destination):
        self.source = source
        self.destination = destination
        print self.filesystem.checkDirExists(destination)

    def getPhotoList(self):
        pass


class ImporterTests(unittest.TestCase):
    source = '~/Programming/Python/event/imagesdir'
    destination = '~/Programming/Python/event/events/rugby/boys'
    
    def setUp(self):
        features.provide('Filesytem', Filesystem)
        self.importer = Importer()
        self.importer.setLocations(self.source, self.destination)

    def testLocations(self):
        self.assertEqual(self.source, self.importer.source)
        self.assertEqual(self.destination, self.importer.destination)

    


def suite():
    testSuite = unittest.makeSuite(ImporterTests)
    return testSuite

        
if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
