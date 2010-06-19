import unittest

from filesystem import Filesystem
from mocks import MockFilesystem
from featurebroker import *
import os.path

class Importer:
    filesystem = RequiredFeature('Filesystem')

    #Next steps for this class:
    #1. Load pictures from image directory (add test)
    #2. Make it work for pictures that start off portrait
    #3. Use this as a model so importpage can dynamically
    #   update information about import (e.g. import or not?)
    
    pictures = [
        ('imagesdir/DSC_0004.JPG', False, False),
        ('imagesdir/DSC_0009.JPG', True, False),
        ('imagesdir/DSC_0015.JPG', True, False),
        ('imagesdir/DSC_0030.JPG', True, False),
        ]

    index = 0

    def __init__(self):
        pass

    def setLocations(self, source, destination):
        assert self.checkLocationsExist(source, destination), \
            'Source or destination directory does not exist'
        self.source = source
        self.destination = destination
        #for item in self.filesystem.listJpegs(self.source):
        #    print item

    def getPictures(self):
        return self.pictures

    def __iter__(self):
        return self

    def checkLocationsExist(self, source, destination):
        return self.filesystem.checkDirExists(source) and \
            self.filesystem.checkDirExists(destination)


class ImporterTests(unittest.TestCase):
    source = 'imagesdir'
    destination = ['events', 'rugby', 'boys']
    
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
