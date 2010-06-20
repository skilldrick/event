import unittest
import sys

from mocks import MockFilesystem
from photo import Orientation
from photo import Photo
from featurebroker import *
import os.path


class Importer:
    filesystem = RequiredFeature('Filesystem')
    pictures = []

    def __init__(self):
        pass

    def setLocations(self, source, destination):
        assert self.checkLocationsExist(source, destination), \
            'Source or destination directory does not exist'
        self.source = str(source)
        self.destination = str(destination)
        self.loadPictures()

    def loadPictures(self):
        for item in self.filesystem.listJpegs(self.source):
            pic = {}
            pic['photo'] = Photo(self.source, item)
            pic['import'] = False
            self.pictures.append(pic)

    def getPictures(self):
        return self.pictures

    def checkLocationsExist(self, source, destination):
        return self.filesystem.checkDirExists(source) and \
            self.filesystem.checkDirExists(destination)

    def setImport(self, index, doImport=True):
        self.pictures[index]['import'] = doImport


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

    def testLoadPictures(self):
        numberOfJpegs = len(list(
                self.importer.filesystem.listJpegs(self.source)))
        numberOfPictures = len(self.importer.pictures)
        self.assertEqual(numberOfJpegs, numberOfPictures)

    def testSetImportTrue(self):
        testIndex = 2
        self.importer.setImport(testIndex)
        self.assertTrue(self.importer.pictures[testIndex]['import'])


def suite():
    testSuite = unittest.makeSuite(ImporterTests)
    return testSuite

        
if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
