import unittest
from PyQt4 import QtCore, QtGui

from featurebroker import *
from config import Config
from filesystem import Filesystem


class Categories(QtGui.QFileSystemModel):
    def __init__(self, widget):
        QtGui.QFileSystemModel.__init__(self, widget)
        self.setFilter(QtCore.QDir.AllDirs |
                       QtCore.QDir.Dirs |
                       QtCore.QDir.NoDotAndDotDot)
        #Need to see if it's possible/worth it to test
        #this class. Maybe, depends how complex it gets.

    def addCategory(self, parent, name):
        return self.mkdir(parent, name)

    def removeCategory(self, categoryIndex):
        return self.rmdir(categoryIndex)


class CategoriesTests(unittest.TestCase):
    def setUp(self):
        self.categories = Categories()


def suite():
    features.provide('Config', Config)
    testSuite = unittest.makeSuite(CategoriesTests)
    return testSuite

    
def main():
    unittest.TextTestRunner().run(suite())

if __name__ == '__main__':
    main()
