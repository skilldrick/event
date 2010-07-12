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



class Importer:
    filesystem = RequiredFeature('Filesystem')

    def __init__(self):
        self.pictures = []
        self.threads = []

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
        thread = ImporterThread(self.pictures, self.destination)
        thread.start()
        self.threads.append(thread)
        thread.progress.connect(self.printProgress)
        if remove:
            thread.finishedProcessing.connect(self.removeImagesFromSource)

    def printProgress(self, progress):
        print 'Progress: ' + str(progress)
            
    def removeImagesFromSource(self):
        for pic in self.pictures:
            path = pic['photo'].path
            self.filesystem.removeFile(path)


class ImporterThread(QtCore.QThread):
    finishedProcessing = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(float)
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
                newPath = [self.destination,
                           self.filesystem.getFilename(path)]
                newPath = self.filesystem.joinPath(newPath)
                self.processImage(pic['photo'], newPath)
        self.finishedProcessing.emit()

    def processImage(self, photo, newPath):
        #print 'Importing ' + newPath
        photo.save(newPath)
        self.currentPic += 1.0
        self.progress.emit(self.currentPic / self.importablePics)
        #print 'Imported ' + newPath
        #self.exec_()
    

            
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
        self.importer.setImport(7)
        self.importer.importSelected()
        time.sleep(0.01) #should be enough of a sleep for importing
        if not self.countJpegsInDestination():
            time.sleep(0.1) #try a longer sleep if necessary
        self.assertEqual(self.countJpegsInDestination(), 1)
        self.reset.empty(self.destination,
                         removeDir=False)
        self.assertEqual(self.countJpegsInDestination(), 0)

    def testRemoveImagesFromSource(self):
        self.assertTrue(self.countJpegsInSource > 0)
        self.importer.removeImagesFromSource()
        self.assertTrue(self.countJpegsInSource() == 0)
        self.reset.fill()

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
