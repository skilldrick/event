from PyQt4 import QtCore, QtGui

from featurebroker import *

class ImportPage(QtGui.QWidget):
    config = RequiredFeature('Config')
    importer = RequiredFeature('Importer')
    widgets = []
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupLayout()

    def setupLayout(self):
        self.label = QtGui.QLabel('hello')
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.setLayout(self.vbox)

    def setSourceDest(self, source, destination):
        self.importer.setLocations(source, destination)
        self.displayPictures()

    def displayPictures(self):
        for pic in self.importer:
            self.widgets.append(PhotoListWidget(pic))
        for widget in self.widgets:
            self.vbox.addWidget(widget)
        self.setLayout(self.vbox)
        
    
class PhotoListWidget(QtGui.QWidget):
    def __init__(self, path, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.imagePath = path
        self.setupLayout()

    def setupLayout(self):
        pixmap = QtGui.QPixmap(self.imagePath)
        label = QtGui.QLabel('', self)
        label.setPixmap(pixmap)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(label)
        self.setLayout(hbox)

