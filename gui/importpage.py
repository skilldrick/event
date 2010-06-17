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
    thumbSize = 100
    
    def __init__(self, imagePath, imageRotation, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.path = imagePath
        self.rotation = imageRotation
        self.setupLayout()

    def setupLayout(self):
        #this assumes that all input images will be landscape,
        #with possible rotation metadata. Images that are actually
        #portrait will probably come through cropped.
        self.label = QtGui.QLabel('Loading ...', self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setFixedSize(self.thumbSize, self.thumbSize)
        #self.label.setFrameStyle(QtGui.QFrame.Panel)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.label)
        self.setLayout(hbox)
        #self.loadPhoto()

    def loadPhoto(self):
        image = QtGui.QImage(self.path)
        thumb = image.scaledToWidth(self.thumbSize)
                                    QtCore.Qt.SmoothTransformation)
        pixmap = QtGui.QPixmap(thumb)

        if self.rotation:
            transform = QtGui.QTransform().rotate(90)
            pixmap = pixmap.transformed(transform)
        self.label.setPixmap(pixmap)

        

    
class PhotoWidgetList(QtGui.QWidget):
    importer = RequiredFeature('Importer')

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.timer = QtCore.QTimer(self)
        self.photoWidgets = []
        self.currentIndex = 0
        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)

    def setSourceDest(self, source, destination):
        self.importer.setLocations(source, destination)

    def display(self):
        #limit number to display for testing
        for i, pic in enumerate(self.importer):
            if i < 4:
                self.addPhoto(pic[0], pic[1])
        self.loadPhotos()

    def loadPhotos(self):
        self.timer.singleShot(100, self.loadPhotoByIndex)

    def loadPhotoByIndex(self):
        if self.currentIndex < len(self.photoWidgets):
            currentPhoto = self.photoWidgets[self.currentIndex]
            currentPhoto.loadPhoto()
            self.currentIndex += 1
            self.timer.singleShot(100,
                                  self.loadPhotoByIndex)

    def addPhoto(self, imagePath, imageRotation):
        hbox = QtGui.QHBoxLayout()
        photoWidget = PhotoWidget(imagePath, imageRotation)
        self.photoWidgets.append(photoWidget)
        hbox.addWidget(photoWidget)
        load = QtGui.QPushButton('Load')
        load.clicked.connect(photoWidget.loadPhoto)
        hbox.addWidget(load)
        self.vbox.addLayout(hbox)
        self.setLayout(self.vbox)
        # As recommended by http://doc.trolltech.com/4.6/qscrollarea.html:
        self.setMinimumSize(self.sizeHint())


