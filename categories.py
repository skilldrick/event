import unittest
from PyQt4 import QtCore, QtGui

from featurebroker import *
from config import Config
from filesystem import Filesystem


class Categories(QtGui.QFileSystemModel):
    def __init__(self, parent):
        QtGui.QFileSystemModel.__init__(self, parent)
        self.setFilter(QtCore.QDir.AllDirs |
                       QtCore.QDir.Dirs |
                       QtCore.QDir.NoDotAndDotDot)
        #Need to see if it's possible/worth it to test
        #this class. Maybe, depends how complex it gets.

        """
        Implement a way to add a new dir. Maybe through
        filesystem.py? Then send a signal to CategoriesPage
        to update. Or edit the treeview?
        """

    def addEvent(self):
        parent = self.index(0, 0, QtCore.QModelIndex())
        print parent.data().toString()
        #print 'newEvent', parent
        #self.mkdir(parent, 'newEvent')


class CategoriesTests(unittest.TestCase):
    def setUp(self):
        self.categories = Categories()


def suite():
    #features.provide('Filesystem', MockFilesystem)
    features.provide('Config', Config)
    testSuite = unittest.makeSuite(CategoriesTests)
    return testSuite

    
def main():
    unittest.TextTestRunner().run(suite())

if __name__ == '__main__':
    main()
