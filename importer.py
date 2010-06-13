import unittest

from filesystem import Filesystem
from mocks import MockFilesystem
from featurebroker import *
import os.path

class Importer:
    filesystem = RequiredFeature('Filesystem')

    pictures = [
        ('imagesdir/DSC_0004.JPG', False, False),
        ('imagesdir/DSC_0009.JPG', True, False),
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

    def next(self):
        oldIndex = self.index
        self.index += 1
        if self.index > len(self.pictures):
            raise StopIteration
        return self.pictures[oldIndex]

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

"""
class MyIterator:
    things = ['purple', 'monkey', 'dishwasher']
    index = -1

    def next(self):
        self.index += 1
        if self.index >= len(self.things):
            raise StopIteration
        return self.things[self.index]

    def __iter__(self):
        return self

it = MyIterator()

for item in it:
    print item
""" 


def suite():
    testSuite = unittest.makeSuite(ImporterTests)
    return testSuite

        
if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
