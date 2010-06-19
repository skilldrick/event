import unittest
import sys

from mocks import MockFilesystem
from photo import Orientation
from photo import Photo
from featurebroker import *
import os.path


class Importer:
    filesystem = RequiredFeature('Filesystem')

    #Next steps for this class:
    #[1. Load pictures from image directory (badd test)] DONE
    #2. Make it work for pictures that start off portrait
    #(to do this make the changes to ThumbMaker on importpage.
    #3. Use this as a model so importpage can dynamically
    #   update information about import (e.g. import or not?)

    pictures = []

    def __init__(self):
        pass

    def setLocations(self, source, destination):
        assert self.checkLocationsExist(source, destination), \
            'Source or destination directory does not exist'
        self.source = source
        self.destination = destination
        self.loadPictures()

    def loadPictures(self):
        for item in self.filesystem.listJpegs(self.source):
            pic = {}
            pic['photo'] = Photo(self.source, item)
            #pic['path'] = self.filesystem.joinPath([self.source, item])
            pic['import'] = False
            self.pictures.append(pic)

    def getPictures(self):
        return self.pictures

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

    def testLoadPictures(self):
        numberOfJpegs = len(list(
                self.importer.filesystem.listJpegs(self.source)))
        numberOfPictures = len(self.importer.pictures)
        self.assertEqual(numberOfJpegs, numberOfPictures)


def suite():
    testSuite = unittest.makeSuite(ImporterTests)
    return testSuite

        
if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
