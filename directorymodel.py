import unittest
from PyQt4 import QtCore, QtGui

from featurebroker import *
from config import Config
from filesystem import Filesystem


class DirectoryModel(QtGui.QFileSystemModel):
    config = RequiredFeature('Config')
    
    def __init__(self, widget, eventName=''):
        QtGui.QFileSystemModel.__init__(self, widget)
        self.setFilter(QtCore.QDir.AllDirs |
                       QtCore.QDir.Dirs |
                       QtCore.QDir.NoDotAndDotDot)

    def addItem(self, parent, name):
        return self.mkdir(parent, name)

    def removeItem(self, categoryIndex):
        return self.rmdir(categoryIndex)


class DirectoryModelTests(unittest.TestCase):
    def setUp(self):
        self.directoryModel = DirectoryModel()


def suite():
    features.provide('Config', Config)
    testSuite = unittest.makeSuite(DirectoryModelTests)
    return testSuite

    
def main():
    unittest.TextTestRunner().run(suite())

if __name__ == '__main__':
    main()
