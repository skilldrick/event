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
        """
        scrollArea = QtGui.QScrollArea()
        self.photoWidgetList = PhotoWidgetList()
        scrollArea.setWidget(self.photoWidgetList)
        outerBox = QtGui.QVBoxLayout()
        outerBox.addWidget(scrollArea)
        self.setLayout(outerBox)
        """
        scrollArea = QtGui.QScrollArea()
        self.photoWidgetList = PhotoWidgetList()
        scrollArea.setWidget(self.photoWidgetList)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(scrollArea)
        self.setLayout(vbox)

    def setSourceDest(self, source, destination):
        self.importer.setLocations(source, destination)
        self.displayPictures()

    def displayPictures(self):
        for pic in self.importer:
            self.photoWidgetList.addPhoto(pic[0], pic[1])


class PhotoWidget(QtGui.QWidget):
    def __init__(self, imagePath, imageRotation, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.path = imagePath
        self.rotation = imageRotation
        self.setupLayout()

    def setupLayout(self):
        pixmap = QtGui.QPixmap(self.path)
        if self.rotation:
            transform = QtGui.QTransform().rotate(90)
            pixmap = pixmap.transformed(transform)
        pixmap = pixmap.scaledToHeight(100, QtCore.Qt.SmoothTransformation)
        label = QtGui.QLabel('', self)
        label.setPixmap(pixmap)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(label)
        self.setLayout(hbox)

    
class PhotoWidgetList(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)

    def addPhoto(self, imagePath, imageRotation):
        self.vbox.addWidget(PhotoWidget(imagePath, imageRotation))
        self.setLayout(self.vbox)
        self.setMinimumSize(self.sizeHint())

