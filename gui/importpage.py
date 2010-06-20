from PyQt4 import QtCore, QtGui
import math

from featurebroker import *
from photo import Orientation

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
        self.photoWidgetList.display()


class PhotoWidget(QtGui.QWidget):
    config = RequiredFeature('Config')
    setImport = QtCore.pyqtSignal(int, bool)
    
    def __init__(self, photo, index, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.photo = photo
        self.index = index
        self.thumbSize = self.config.getProperty('thumbsize')
        self.setupLayout()

    def setupLayout(self):
        self.label = QtGui.QLabel('Loading ...', self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setFixedSize(self.thumbSize, self.thumbSize)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.label)
        checkbox = QtGui.QCheckBox()
        checkbox.stateChanged.connect(self.stateChanged)

        hbox.addWidget(checkbox)
        self.setLayout(hbox)

    def stateChanged(self, state):
        if state == QtCore.Qt.Unchecked:
            state = False
        else:
            state = True
        self.setImport.emit(self.index, state)

    def displayPhoto(self, image):
        orientation = self.photo.getOrientation()
        pixmap = QtGui.QPixmap(image)
        self.label.setPixmap(pixmap)


class PhotoWidgetList(QtGui.QWidget):
    importer = RequiredFeature('Importer')

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.timer = QtCore.QTimer(self)
        self.photoWidgets = []
        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)

    def setSourceDest(self, source, destination):
        self.importer.setLocations(source, destination)

    def display(self):
        for i, pic in enumerate(self.importer.getPictures()):
            self.addPhoto(pic['photo'], i)

        self.setLayout(self.vbox)
        # As recommended by http://doc.trolltech.com/4.6/qscrollarea.html:
        self.setMinimumSize(self.sizeHint())
        self.loadPhotos()

    def displayPhoto(self, thumb, index):
        self.photoWidgets[index].displayPhoto(thumb)

    def loadPhotos(self):
        photos = [widget.photo for widget in self.photoWidgets]
        self.thread = ThumbMakerThread(photos)
        self.thread.madeThumb.connect(self.displayPhoto)
        self.thread.start()

    def addPhoto(self, photo, index):
        photoWidget = PhotoWidget(photo, index)
        photoWidget.setImport.connect(self.importer.setImport)
        self.photoWidgets.append(photoWidget)
        self.vbox.addWidget(photoWidget)


class ThumbMaker(QtCore.QObject):
    config = RequiredFeature('Config')

    def __init__(self, path, orientation):
        QtCore.QObject.__init__(self)
        self.orientation = orientation
        self.path = path
        self.thumbSize = self.config.getProperty('thumbsize')

    def unRotated(self):
        return orientation == Orientation.LANDSCAPE or \
            orientation == Orientation.PORTRAIT

    def rotatedCW(self):
        return self.orientation == Orientation.CW_LANDSCAPE or \
            self.orientation == Orientation.CW_PORTRAIT

    def rotatedCCW(self):
        return self.orientation == Orientation.CCW_LANDSCAPE or \
            self.orientation == Orientation.CCW_PORTRAIT

    def rotated180(self):
        return self.orientation == Orientation.FLIPPED_LANDSCAPE or \
            self.orientation == Orientation.FLIPPED_PORTRAIT

    def makeThumb(self):
        image = QtGui.QImage(self.path)
        assert not image.isNull(), 'Image in ' + self.path + ' is null'

        if self.rotatedCW():
            transform = QtGui.QTransform().rotate(270)
            image = image.transformed(transform)
        elif self.rotatedCCW():
            transform = QtGui.QTransform().rotate(90)
            image = image.transformed(transform)
        elif self.rotated180():
            transform = QtGui.QTransform().rotate(180)
            image = image.transformed(transform)
            
        if self.orientation == 1 or \
                self.orientation == 2 or \
                self.orientation == 4:
            thumb = image.scaledToHeight(self.thumbSize,
                                         QtCore.Qt.SmoothTransformation)
        else:
            thumb = image.scaledToWidth(self.thumbSize,
                                         QtCore.Qt.SmoothTransformation)
        return thumb
        

class ThumbMakerThread(QtCore.QThread):
    madeThumb = QtCore.pyqtSignal(QtGui.QImage, int)
    
    def __init__(self, photos):
        QtCore.QThread.__init__(self)
        self.photos = photos
    
    def run(self):
        for i, photo in enumerate(self.photos):
            thumbMaker = ThumbMaker(photo.getPath(),
                                    photo.getOrientation())
            self.madeThumb.emit(thumbMaker.makeThumb(), i)
        self.exec_()

    
