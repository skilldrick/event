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
    config = RequiredFeature('Config')
    
    def __init__(self, imagePath, imageRotation, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.path = imagePath
        self.rotation = imageRotation
        self.thumbSize = self.config.getProperty('thumbsize')
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

    def loadPhoto(self, image):
        pixmap = QtGui.QPixmap(image)
        if self.rotation:
            transform = QtGui.QTransform().rotate(90)
            pixmap = pixmap.transformed(transform)
        self.label.setPixmap(pixmap)


class PhotoMaker(QtCore.QObject):
    config = RequiredFeature('Config')

    def __init__(self, path):
        QtCore.QObject.__init__(self)
        self.path = path
        self.thumbSize = self.config.getProperty('thumbsize')

    def makeThumb(self):
        image = QtGui.QImage(self.path)
        thumb = image.scaledToWidth(self.thumbSize,
                                    QtCore.Qt.SmoothTransformation)
        return thumb
        

class MyQThread(QtCore.QThread):
    madeThumb = QtCore.pyqtSignal(QtGui.QImage, int)
    
    def __init__(self, paths):
        QtCore.QThread.__init__(self)
        self.paths = paths
    
    def run(self):
        for i, path in enumerate(self.paths):
            photoMaker = PhotoMaker(path)
            self.madeThumb.emit(photoMaker.makeThumb(), i)
        self.exec_()

    
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
        for pic in self.importer.getPictures():
            self.addPhoto(pic[0], pic[1])
        self.loadPhotos()

    def loadPhoto(self, thumb, index):
        self.photoWidgets[index].loadPhoto(thumb)

    def loadPhotos(self):
        paths = [widget.path for widget in self.photoWidgets]
        self.thread = MyQThread(paths)
        self.thread.madeThumb.connect(self.loadPhoto)
        self.thread.start()

    def addPhoto(self, imagePath, imageRotation):
        hbox = QtGui.QHBoxLayout()
        photoWidget = PhotoWidget(imagePath, imageRotation)
        self.photoWidgets.append(photoWidget)
        hbox.addWidget(photoWidget)
        #add buttons etc. to the hbox now.
        self.vbox.addLayout(hbox)
        self.setLayout(self.vbox)
        # As recommended by http://doc.trolltech.com/4.6/qscrollarea.html:
        self.setMinimumSize(self.sizeHint())


