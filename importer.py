from PyQt4 import QtCore
import unittest
import sys
import time

from mocks import MockFilesystem
from filesystem import Filesystem
from photo import Orientation
from photo import Photo
from featurebroker import *
import os.path
from reset import Reset



class ImportList(QtCore.QObject):
    filesystem = RequiredFeature('Filesystem')

    def __init__(self):
        QtCore.QObject.__init__(self)
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

    def getImporter(self):
        return Importer(self.pictures, self.destination)


class Importer(QtCore.QObject):
    filesystem = RequiredFeature('Filesystem')
    importProgress = QtCore.pyqtSignal(int)
    removeProgress = QtCore.pyqtSignal(int)
    finishedImporting = QtCore.pyqtSignal()
    
    def __init__(self, pictures, destination):
        QtCore.QObject.__init__(self)
        self.threads = []
        self.pictures = pictures
        self.destination = destination
        self.currentPic = 0

    def importSelected(self, remove=True):
        thread = ImporterThread(self.pictures, self.destination)
        thread.start()
        self.threads.append(thread)
        thread.importProgress.connect(self.importProgress)
        thread.finishedImporting.connect(self.finishedImporting)

    def removeImagesFromSource(self):
        for pic in self.pictures:
            path = pic['photo'].path
            self.filesystem.removeFile(path)
            self.currentPic += 1.0
            progress = 100 * (self.currentPic / len(self.pictures))
            self.removeProgress.emit(progress)


class ImporterThread(QtCore.QThread):
    finishedImporting = QtCore.pyqtSignal()
    importProgress = QtCore.pyqtSignal(int)
    filesystem = RequiredFeature('Filesystem')
    
    def __init__(self, pictures, destination, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.pictures = pictures
        self.destination = destination
        self.importablePics = len([pic for pic in self.pictures
                                   if pic['import']])
        self.currentPic = 0

    def run(self):
        for pic in self.pictures:
            if pic['import']:
                path = pic['photo'].path
                self.processImage(pic['photo'])
        self.finishedImporting.emit()

    def getFileNumber(self, filename):
        filename = str(filename)
        number = filename[-7:-4]
        return int(number)

    def getLastFileNumber(self):
        filenames = self.filesystem.listJpegs(self.destination)
        filenames = list(filenames)
        if len(filenames) > 0:
            filenumbers = [self.getFileNumber(filename)
                           for filename in filenames]
            return max(filenumbers)
        else:
            return 0

    def getNextFilename(self):
        newNumber = self.getLastFileNumber() + 1
        #see http://docs.python.org/library/string.html#format-examples
        return "Photo {0:0>3}.jpg".format(newNumber)
        
    def processImage(self, photo):
        newPath = [self.destination,
                   self.getNextFilename()]
        photo.save(newPath)
        self.currentPic += 1.0
        #emit percentage progress:
        progress = 100 * (self.currentPic / self.importablePics)
        self.importProgress.emit(int(progress))


class ImportListTests(unittest.TestCase):
    filesystem = Filesystem()
    source = 'imagesdir'
    destination = ['events', 'rugby', 'boys']
    reset = Reset()
    
    def setUp(self):
        features.provide('Filesystem', MockFilesystem)
        if not self.filesystem.checkDirExists(self.destination):
            self.filesystem.makeDir(self.destination)
        self.importList = ImportList()
        self.importList.setLocations(self.source, self.destination)

    def testLocations(self):
        self.assertEqual(self.source, self.importList.source)
        self.assertEqual(self.destination, self.importList.destination)
        self.assertTrue(self.importList.checkLocationExists(self.source))
        self.assertTrue(self.importList.checkLocationExists(self.destination))

    def testLoadPictures(self):
        numberOfJpegs = len(list(
                self.importList.filesystem.listJpegs(self.source)))
        numberOfPictures = len(self.importList.pictures)
        self.assertEqual(numberOfJpegs, numberOfPictures)

    def testSetImportTrue(self):
        testIndex = 2
        self.importList.setImport(testIndex)
        self.assertTrue(self.importList.pictures[testIndex]['import'])

    """
    #This is now handled from importpage.
    def testImportSelectedAndRemoveImagesFromSource(self):
        self.reset.empty(self.destination,
                         removeDir=False)
        self.importList.setImport(7)
        self.importList.importSelected()
        time.sleep(0.01) #should be enough of a sleep for importing
        if not self.countJpegsInDestination():
            time.sleep(0.1) #try a longer sleep if necessary
        self.assertEqual(self.countJpegsInDestination(), 1)
        #self.assertEqual(self.countJpegsInSource(), 0)
        self.reset.empty(self.destination,
                         removeDir=False)
        self.assertEqual(self.countJpegsInDestination(), 0)
    """

    def countJpegsInDestination(self):
        return self.countJpegsInDirectory(self.destination)

    def countJpegsInSource(self):
        return self.countJpegsInDirectory(self.source)

    def countJpegsInDirectory(self, directory):
        files = self.filesystem.listJpegs(directory)
        return len(list(files))


class ImporterTests(unittest.TestCase):
    def setUp(self):
        pass


def suite():
    importListTestSuite = unittest.makeSuite(ImportListTests)
    importerTestSuite = unittest.makeSuite(ImporterTests)
    testSuite = unittest.TestSuite((importListTestSuite, importerTestSuite))
    return testSuite

        
if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
