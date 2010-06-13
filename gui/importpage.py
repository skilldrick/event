from PyQt4 import QtCore, QtGui
import math

from featurebroker import *

class ImportPage(QtGui.QWidget):
    config = RequiredFeature('Config')
    importer = RequiredFeature('Importer')
    widgets = []
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupLayout()

    def setupLayout(self):
        self.vbox = QtGui.QVBoxLayout()
        #use a QScrollArea here.
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
    def __init__(self, pic, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.imagePath = pic[0]
        self.rotation = pic[1]
        self.setupLayout()

    def setupLayout(self):
        pixmap = QtGui.QPixmap(self.imagePath).scaledToHeight(100,
                                                              QtCore.Qt.SmoothTransformation)
        if self.rotation:
            transform = QtGui.QTransform().rotate(90)
            pixmap = pixmap.transformed(transform)
        label = QtGui.QLabel('', self)
        label.setPixmap(pixmap)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(label)
        self.setLayout(hbox)

