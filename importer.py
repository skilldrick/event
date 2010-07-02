import unittest
import sys

from mocks import MockFilesystem
from filesystem import Filesystem
from photo import Orientation
from photo import Photo
from featurebroker import *
import os.path
from reset import Reset


class Importer:
    filesystem = RequiredFeature('Filesystem')

    def __init__(self):
        self.pictures = []

    def setLocations(self, source, destination):
        assert self.checkLocationExists(source), \
            'Source directory does not exist'
        assert self.checkLocationExists(destination), \
            'Destination directory does not exist'
        self.source = source
        self.destination = destination
        self.loadPictures()

    def loadPictures(self):
        for item in self.filesystem.listJpegs(self.source):
            pic = {}
            pic['photo'] = Photo(self.source, item)
            pic['import'] = False
            self.pictures.append(pic)

    def getPictures(self):
        return self.pictures

    def checkLocationExists(self, location):
        return self.filesystem.checkDirExists(location)

    def setImport(self, index, doImport=True):
        self.pictures[index]['import'] = doImport

    def importSelected(self, remove=True):
        for pic in self.pictures:
            if pic['import']:
                path = pic['photo'].path
                newPath = [self.destination,
                           self.filesystem.getFilename(path)]
                self.filesystem.copy(path, newPath)
        if remove:
            self.removeImagesFromSource()

    def removeImagesFromSource(self):
        for pic in self.pictures:
            path = pic['photo'].path
            self.filesystem.removeFile(path)


class ImporterTests(unittest.TestCase):
    filesystem = Filesystem()
    source = 'imagesdir'
    destination = ['events', 'rugby', 'boys']
    reset = Reset()
    
    def setUp(self):
        features.provide('Filesystem', MockFilesystem)
        if not self.filesystem.checkDirExists(self.destination):
            self.filesystem.makeDir(self.destination)
        self.importer = Importer()
        self.importer.setLocations(self.source, self.destination)

    def testLocations(self):
        self.assertEqual(self.source, self.importer.source)
        self.assertEqual(self.destination, self.importer.destination)
        self.assertTrue(self.importer.checkLocationExists(self.source))
        self.assertTrue(self.importer.checkLocationExists(self.destination))

    def testLoadPictures(self):
        numberOfJpegs = len(list(
                self.importer.filesystem.listJpegs(self.source)))
        numberOfPictures = len(self.importer.pictures)
        self.assertEqual(numberOfJpegs, numberOfPictures)

    def testSetImportTrue(self):
        testIndex = 2
        self.importer.setImport(testIndex)
        self.assertTrue(self.importer.pictures[testIndex]['import'])

    def testImportSelected(self):
        self.reset.empty(self.destination,
                         removeDir=False)
        for i in range(3,6):
            self.importer.setImport(i)
        self.importer.importSelected()
        self.assertEqual(self.countJpegsInDestination(), 3)
        self.reset.empty(self.destination,
                         removeDir=False)
        self.assertEqual(self.countJpegsInDestination(), 0)

    def testRemoveImagesFromSource(self):
        self.assertTrue(self.countJpegsInSource > 0)
        self.importer.removeImagesFromSource()
        self.assertTrue(self.countJpegsInSource() == 0)
        self.reset.fill()

    def countJpegsInDestination(self):
        return self.countJpegsInDirectory(self.destination)

    def countJpegsInSource(self):
        return self.countJpegsInDirectory(self.source)

    def countJpegsInDirectory(self, directory):
        files = self.filesystem.listJpegs(directory)
        return len(list(files))


def suite():
    testSuite = unittest.makeSuite(ImporterTests)
    return testSuite

        
if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
