import unittest

from filesystem import Filesystem
from featurebroker import *
import os.path

class Importer:
    filesystem = RequiredFeature('Filesystem')
    
    def __init__(self):
        pass

    def setLocations(self, source, destination):
        self.source = source
        self.destination = destination
        #print self.filesystem.checkDirExists(destination)

    def checkLocationsExist(self, source, destination):
        return self.filesystem.checkDirExists(source)

    def getPhotoList(self):
        pass


class ImporterTests(unittest.TestCase):
    source = 'imagesdir'
    destination = 'events/rugby/boys'
    
    def setUp(self):
        features.provide('Filesystem', Filesystem)
        self.importer = Importer()
        self.importer.setLocations(self.source, self.destination)

    def testLocations(self):
        self.assertEqual(self.source, self.importer.source)
        self.assertEqual(self.destination, self.importer.destination)
        self.assertTrue(self.importer.checkLocationsExist(
                self.source,
                self.destination))

    def testSanity(self):
        self.assertTrue(self.importer.checkLocationsExist(self.destination,
                                                          self.destination))


    


def suite():
    testSuite = unittest.makeSuite(ImporterTests)
    return testSuite

        
if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
