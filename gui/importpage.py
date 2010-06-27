from PyQt4 import QtCore, QtGui
import math

from featurebroker import *
from photo import Orientation
from importer import Importer


class ImportPage(QtGui.QWidget):
    config = RequiredFeature('Config')
    stopLoading = QtCore.pyqtSignal()
    previousPage = QtCore.pyqtSignal()
    importSelected = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupLayout()

    def setupLayout(self):
        self.scrollArea = QtGui.QScrollArea()
        self.selectAllButton = QtGui.QPushButton('Select All')
        self.selectNoneButton = QtGui.QPushButton('Select None')
        topHbox = QtGui.QHBoxLayout()
        topHbox.addStretch()
        topHbox.addWidget(self.selectAllButton)
        topHbox.addWidget(self.selectNoneButton)
        topHbox.addStretch()
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(topHbox)
        vbox.addWidget(self.scrollArea)
        bottomHbox = QtGui.QHBoxLayout()
        backButton = QtGui.QPushButton('Back')
        backButton.clicked.connect(self.previousPage)
        importButton = QtGui.QPushButton('Import selected images')
        importButton.clicked.connect(self.importSelected)
        bottomHbox.addStretch()
        bottomHbox.addWidget(backButton)
        bottomHbox.addWidget(importButton)
        bottomHbox.addStretch()
        vbox.addLayout(bottomHbox)
        self.setLayout(vbox)

    def setSourceDest(self, source, destination):
        """
        setSourceDest is called by a signal from previous page.
        Because it does some stuff in a separate thread, if it is
        called multiple times (e.g. if the user goes back to change
        source or destination) the threads will carry on happily.
        Therefore we need to do some tidying up first. stopLoading
        is connected ultimately to the thumbMakerThread, and will
        cause the thread to stop making thumbs.

        stopLoading is only connected after it is first emitted,
        so will stop the thumbMakerThread associated with the
        previous photoWidgetList. Then photoWidgetList is
        reconstructed with (new) source and destination.
        """
        try:
            #if source is same as last time then don't do anything
            if self.source == source:
                return
        except AttributeError:
            pass
        self.source = source
        self.destination = destination
        self.stopLoading.emit()
        self.photoWidgetList = None

        self.photoWidgetList = PhotoWidgetListMaker()
        self.stopLoading.connect(self.photoWidgetList.stopLoading)
        self.importSelected.connect(self.photoWidgetList.importSelected)
        self.selectAllButton.clicked.connect(self.photoWidgetList.selectAll)
        self.selectNoneButton.clicked.connect(self.photoWidgetList.selectNone)

        self.scrollArea.setWidget(self.photoWidgetList)

        self.photoWidgetList.setSourceDest(source, destination)
        self.photoWidgetList.display()


class PhotoWidget(QtGui.QWidget):
    config = RequiredFeature('Config')
    setImport = QtCore.pyqtSignal(int, bool)
    select = QtCore.pyqtSignal(bool)

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
        self.checkbox = QtGui.QCheckBox()
        self.checkbox.stateChanged.connect(self.stateChanged)
        self.select.connect(self.checkbox.setChecked)

        hbox.addWidget(self.checkbox)
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


def PhotoWidgetListMaker():
    return PhotoWidgetList(Importer())


class PhotoWidgetList(QtGui.QWidget):
    stopLoading = QtCore.pyqtSignal()
    select = QtCore.pyqtSignal(bool)
    importSelected = QtCore.pyqtSignal()
    
    def __init__(self, importer, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.importer = importer
        self.importSelected.connect(self.importer.importSelected)
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
        self.stopLoading.connect(self.thread.stop)
        self.thread.madeThumb.connect(self.displayPhoto)
        self.thread.start()

    def selectAll(self):
        self.select.emit(True)

    def selectNone(self):
        self.select.emit(False)

    def addPhoto(self, photo, index):
        photoWidget = PhotoWidget(photo, index)
        photoWidget.setImport.connect(self.importer.setImport)
        self.select.connect(photoWidget.select)
        self.photoWidgets.append(photoWidget)
        self.vbox.addWidget(photoWidget)


class ThumbMaker(QtCore.QObject):
    config = RequiredFeature('Config')
    """The only thing that hasn't been properly tested in this
    class is images with more obscure exif rotation data.
    Landscape, portrait, and cw-landscape and portrait tested,
    but none of the others, especially those rotated 180 degrees.
    """

    def __init__(self, path, orientation):
        QtCore.QObject.__init__(self)
        self.orientation = orientation
        self.path = path
        self.thumbSize = self.config.getProperty('thumbsize')

    def rotatedCW(self):
        return self.orientation == Orientation.CW_LANDSCAPE or \
            self.orientation == Orientation.CW_PORTRAIT

    def rotatedCCW(self):
        return self.orientation == Orientation.CCW_LANDSCAPE or \
            self.orientation == Orientation.CCW_PORTRAIT

    def rotated180(self):
        return self.orientation == Orientation.FLIPPED_LANDSCAPE or \
            self.orientation == Orientation.FLIPPED_PORTRAIT

    def scaleByHeight(self):
        return self.orientation == Orientation.PORTRAIT or \
            self.orientation == Orientation.CW_LANDSCAPE or \
            self.orientation == Orientation.CCW_LANDSCAPE or \
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
            
        if self.scaleByHeight():
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
        self.stopLoading = False

    def stop(self):
        #on next iteration stop loading images
        self.stopLoading = True

    def run(self):
        for i, photo in enumerate(self.photos):
            if self.stopLoading:
                break
            thumbMaker = ThumbMaker(photo.getPath(),
                                    photo.getOrientation())
            self.madeThumb.emit(thumbMaker.makeThumb(), i)
    
        self.exec_()
