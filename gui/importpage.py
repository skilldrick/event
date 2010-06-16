from PyQt4 import QtCore, QtGui
import math

from featurebroker import *

class ImportPage(QtGui.QWidget):
    config = RequiredFeature('Config')
    widgets = []
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupLayout()

    def setupLayout(self):
        self.photoWidgetList = PhotoWidgetList()
        scrollArea = QtGui.QScrollArea()
        scrollArea.setWidget(self.photoWidgetList)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(scrollArea)
        self.setLayout(vbox)

    def setSourceDest(self, source, destination):
        self.photoWidgetList.setSourceDest(source, destination)
        self.displayPictures()

    def displayPictures(self):
        self.photoWidgetList.display()


class PhotoWidget(QtGui.QWidget):
    thumbHeight = 100
    
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
        pixmap = pixmap.scaledToHeight(self.thumbHeight,
                                       QtCore.Qt.SmoothTransformation)
        label = QtGui.QLabel('', self)
        label.setPixmap(pixmap)
        #set alignment to horizontal centre
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(label)
        self.setLayout(hbox)

    
class PhotoWidgetList(QtGui.QWidget):
    importer = RequiredFeature('Importer')

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)

    def setSourceDest(self, source, destination):
        self.importer.setLocations(source, destination)

    def display(self):
        #limit number to display for testing
        for i, pic in enumerate(self.importer):
            if i < 2:
                self.addPhoto(pic[0], pic[1])

    def addPhoto(self, imagePath, imageRotation):
        self.vbox.addWidget(PhotoWidget(imagePath, imageRotation))
        self.setLayout(self.vbox)
        # As recommended by http://doc.trolltech.com/4.6/qscrollarea.html:
        self.setMinimumSize(self.sizeHint()) 

