import unittest

from filesystem import Filesystem
from mocks import MockFilesystem
from featurebroker import *
import os.path

class Importer:
    filesystem = RequiredFeature('Filesystem')
    
    def __init__(self):
        pass

    def setLocations(self, source, destination):
        assert(self.checkLocationsExist(source, destination))
        self.source = source
        self.destination = destination
        

    def checkLocationsExist(self, source, destination):
        return self.filesystem.checkDirExists(source)

    def getPhotoList(self):
        pass


class ImporterTests(unittest.TestCase):
    source = 'imagesdir'
    destination = 'events/rugby/boys'
    
    def setUp(self):
        features.provide('Filesystem', MockFilesystem)
        self.importer = Importer()
        self.importer.setLocations(self.source, self.destination)

    def testLocations(self):
        self.assertEqual(self.source, self.importer.source)
        self.assertEqual(self.destination, self.importer.destination)
        self.assertTrue(self.importer.checkLocationsExist(
                self.source,
                self.destination))


    


def suite():
    testSuite = unittest.makeSuite(ImporterTests)
    return testSuite

        
if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
