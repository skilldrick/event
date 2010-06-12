from PyQt4 import QtCore, QtGui

from featurebroker import *

class ImportPage(QtGui.QWidget):
    config = RequiredFeature('Config')
    importer = RequiredFeature('Importer')
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupLayout()

    def setupLayout(self):
        self.label = QtGui.QLabel('hello')
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.label)
        self.setLayout(vbox)

    def setSourceDest(self, source, destination):
        self.importer.setLocations(source, destination)
        self.importer.getPhotoList()
