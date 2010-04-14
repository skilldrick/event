from PyQt4 import QtCore, QtGui

from featurebroker import *

class CategoriesPage(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupLayout()

    def setupLayout(self):
        self.model = QtGui.QFileSystemModel(self)
        self.model.setRootPath('~/Programming/Python/event/events')
        
        
