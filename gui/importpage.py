from PyQt4 import QtCore, QtGui
import math
import time

from featurebroker import *
from photo import Orientation
from importer import ImportList


class ImportPage(QtGui.QWidget):
    config = RequiredFeature('Config')
    stopLoading = QtCore.pyqtSignal()
    previousPage = QtCore.pyqtSignal()
    restart = QtCore.pyqtSignal()
    
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

    def importSelected(self):
        #Sorry Demeter!
        self.importer = self.photoWidgetList.importList.getImporter()
        self.importer.finishedImporting.connect(self.finishedImporting)
        self.importer.finishedRemoving.connect(self.finishedRemoving)
        self.importer.importCancelled.connect(self.importCancelled)
        self.restart.connect(self.photoWidgetList.importList.close)
        self.showImportProgressBar()
        self.importer.importSelected()

    def showImportProgressBar(self):
        self.setDisabled(True)
        self.importProgressWidget = ProgressWidget('Importing', self)
        self.importer.importProgress.connect(
            self.importProgressWidget.setProgress)
        self.importProgressWidget.rejected.connect(
            self.importer.cancelImport)
        self.importProgressWidget.show()

    def removeImages(self, removeSelected=False):
        self.showRemoveProgressBar()
        self.importer.removeImagesFromSource(removeSelected)

    def showRemoveProgressBar(self):
        self.removeProgressWidget = ProgressWidget(
            'Deleting images', self)
        self.importer.removeProgress.connect(
            self.removeProgressWidget.setProgress)
        self.removeProgressWidget.rejected.connect(
            self.importer.cancelRemove)
        self.removeProgressWidget.show()

    def finishedImporting(self):
        self.importProgressWidget.close()
        title = 'Delete images?'
        message = 'Delete all images from source directory,\n'
        message += 'only the selected images, or keep all the images?'
        messageBox = QtGui.QMessageBox(self)
        messageBox.setWindowTitle(title)
        messageBox.setText(message)
        messageBox.setIcon(QtGui.QMessageBox.Question)
        deleteAll = messageBox.addButton(
            'Delete All', QtGui.QMessageBox.AcceptRole)
        deleteSelected = messageBox.addButton(
            'Delete Selected', QtGui.QMessageBox.AcceptRole)
        keepAll = messageBox.addButton(
            'Keep All', QtGui.QMessageBox.RejectRole)
        messageBox.exec_()
        if messageBox.clickedButton() == deleteAll:
            self.removeImages()
        elif messageBox.clickedButton() == deleteSelected:
            self.removeImages(removeSelected=True)
        else:
            self.finished()

    def importCancelled(self):
        self.importProgressWidget.close()
        title = 'Import cancelled'
        message = 'You have cancelled importing the selected images.\n'
        message += 'Any images already imported have been removed.'
        QtGui.QMessageBox.information(self, title, message)
        self.setDisabled(False)
        
    def finishedRemoving(self):
        self.removeProgressWidget.close()
        self.finished()

    def finished(self):
        title = 'Finished importing/deleting'
        message = 'Importing/deleting complete.\n'
        message += 'Click OK to return to the start page.'
        QtGui.QMessageBox.information(self, title, message)
        self.setDisabled(False)
        self.restart.emit()

    def setSourceDest(self, source, destination):
        try:
            oldSource = self.source
        except AttributeError:
            oldSource = None
            
        self.source = source
        self.destination = destination

        #First time:
        if oldSource == None:
            self.setupPhotoWidgetList()
        #Subsequent times, but only if source has changed:
        elif oldSource != self.source:
            #Need to stop thumbMakerThread from loading thumbs:
            self.stopLoading.emit()
            self.setupPhotoWidgetList()
        else:
            #Source hasn't changed so no need to setup photowidgetlist
            pass

    def setupPhotoWidgetList(self):
        self.photoWidgetList = PhotoWidgetListMaker()
        self.stopLoading.connect(self.photoWidgetList.stopLoading)
        
        self.selectAllButton.clicked.connect(
            self.photoWidgetList.selectAll)
        self.selectNoneButton.clicked.connect(
            self.photoWidgetList.selectNone)

        self.scrollArea.setWidget(self.photoWidgetList)

        self.photoWidgetList.setSourceDest(self.source, self.destination)
        self.photoWidgetList.display()


class ProgressWidget(QtGui.QDialog):
    def __init__(self, text, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.text = text
        self.setWindowTitle(text)
        self.setupLayout()

    def setupLayout(self):
        self.setWindowModality(True)
        vbox = QtGui.QVBoxLayout()
        self.label = QtGui.QLabel(self.text)
        self.progressBar = QtGui.QProgressBar()
        self.cancelButton = QtGui.QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.reject)
        vbox.addWidget(self.label)
        vbox.addWidget(self.progressBar)
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.cancelButton)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def setProgress(self, progress):
        self.progressBar.setValue(progress)


def PhotoWidgetListMaker():
    return PhotoWidgetList(ImportList())


class PhotoWidgetList(QtGui.QWidget):
    stopLoading = QtCore.pyqtSignal()
    select = QtCore.pyqtSignal(bool)
    
    def __init__(self, importList, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.importList = importList
        self.photoWidgets = []
        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)

    def setSourceDest(self, source, destination):
        self.importList.setLocations(source, destination)

    def display(self):
        for i, pic in enumerate(self.importList.getPictures()):
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
        photoWidget.setImport.connect(self.importList.setImport)
        self.select.connect(photoWidget.select)
        self.photoWidgets.append(photoWidget)
        self.vbox.addWidget(photoWidget)


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
        pixmap = QtGui.QPixmap(image)
        self.label.setPixmap(pixmap)


class ThumbMaker(QtCore.QObject):
    config = RequiredFeature('Config')
    """The only thing that hasn't been properly tested in this
    class is images with more obscure exif rotation data.
    Landscape, portrait, and cw-landscape and portrait tested,
    but none of the others, especially those rotated 180 degrees.
    """

    def __init__(self, photo):
        QtCore.QObject.__init__(self)
        self.photo = photo
        self.path = photo.getPath()
        self.thumbSize = self.config.getProperty('thumbsize')

    def scaleByHeight(self):
        return self.photo.orientation == Orientation.PORTRAIT or \
            self.photo.orientation == Orientation.CW_LANDSCAPE or \
            self.photo.orientation == Orientation.CCW_LANDSCAPE or \
            self.photo.orientation == Orientation.FLIPPED_PORTRAIT

    def makeThumb(self):
        assert self.path != '', self.path + ' doesn\'t exist'
        image = QtGui.QImage(self.path)
        assert not image.isNull(), 'Image in ' + self.path + ' is null'

        if self.photo.rotatedCW():
            transform = QtGui.QTransform().rotate(270)
            image = image.transformed(transform)
        elif self.photo.rotatedCCW():
            transform = QtGui.QTransform().rotate(90)
            image = image.transformed(transform)
        elif self.photo.rotated180():
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
            thumbMaker = ThumbMaker(photo)
            self.madeThumb.emit(thumbMaker.makeThumb(), i)
    
        self.exec_()
