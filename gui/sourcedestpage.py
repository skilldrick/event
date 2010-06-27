from PyQt4 import QtCore, QtGui

from featurebroker import *
from directorymodel import DirectoryModel
import functions
from .shared import Shared


class SourceWidget(Shared):
    model = RequiredFeature('SourceList')
    itemStrings = {'itemRemoveFailed':'Could not remove this source.',
                   'singularCaps': 'Source',
                   'singularLower': 'source',
                   'pluralCaps': 'Sources',
                   'pluralLower': 'sources',
                   }
    
    def __init__(self, parent=None):
        Shared.__init__(self, parent)
        self.setupLayout()

    def setupLayout(self):
        self.view = QtGui.QListView()
        self.view.setModel(self.model)
        self.addButton = QtGui.QPushButton('Add source')
        self.addButton.clicked.connect(self.getItem)
        self.removeButton = QtGui.QPushButton('Remove source')
        self.removeButton.clicked.connect(self.removeItem)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.view)
        vbox.addWidget(self.addButton)
        vbox.addWidget(self.removeButton)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)

    def getItem(self):
        title = 'New source'
        path = QtGui.QFileDialog.getExistingDirectory(self, title)
        path = str(path)
        if len(path) == 0: #no directory selected
            return

        body = 'Please give this source a name:'
        name = QtGui.QInputDialog.getText(self, title, body)[0]
        name = str(name)
        if len(name) > 0:
            self.addItem(path, name)

    def addItem(self, path, name):
        self.model.addItem(path, name)

    def getSelectedPath(self):
        index = self.getSelectedIndex()
        if index:
            return self.model.data(index, QtCore.Qt.UserRole)
        

class DeselectableTreeView(QtGui.QTreeView):
    def mousePressEvent(self, event):
        """When the TreeView is clicked, the selection is cleared.
        If an item is clicked, QTreeView.mousePressEvent() selects it"""
        self.clearSelection()
        QtGui.QTreeView.mousePressEvent(self, event)


class CategoryWidget(Shared):
    config = RequiredFeature('Config')
    filesystem = RequiredFeature('Filesystem')
    itemStrings = {'singularCaps': 'Category',
                   'singularLower': 'category',
                   'pluralCaps': 'Categories',
                   'pluralLower': 'categories',
                   }

    def __init__(self, parent=None):
        Shared.__init__(self, parent)
        self.setupLayout()

    def setupLayout(self):
        self.view = DeselectableTreeView()
        self.addButton = QtGui.QPushButton('Add category')
        self.addButton.clicked.connect(self.getItem)
        self.removeButton = QtGui.QPushButton('Remove category')
        self.removeButton.clicked.connect(self.removeItem)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.view)
        vbox.addWidget(self.addButton)
        vbox.addWidget(self.removeButton)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)
        
    def setEvent(self, eventName):
        eventName = str(eventName)
        self.model = DirectoryModel(self, eventName)
        self.view.setModel(self.model)
        for col in range(1, 4):
            self.view.hideColumn(col)
        self.view.setHeaderHidden(True)
        currentEventPath = self.filesystem.joinPath([
                self.config.eventsDir(),
                eventName,
                ])
        self.model.setRootPath(currentEventPath)
        currentPathIndex = self.model.index(currentEventPath)
        self.view.setRootIndex(currentPathIndex)
        
    def addItem(self, categoryName):
        selectedIndex = self.getSelectedIndex()
        if not selectedIndex:
            selectedIndex = self.view.rootIndex()
        success = self.model.addItem(selectedIndex, categoryName)
        if not success:
            print 'addItem failed'

    def getSelectedPath(self):
        index = self.getSelectedIndex()
        if index:
            qVariant = self.model.data(index,
                                       QtGui.QFileSystemModel.FilePathRole)
            return qVariant.toString()
            
        
class SourceDestPage(QtGui.QWidget):
    config = RequiredFeature('Config')
    sourceList = RequiredFeature('SourceList')
    previousPage = QtCore.pyqtSignal()
    nextPage = QtCore.pyqtSignal()
    setEvent = QtCore.pyqtSignal(str)
    setSourceDest = QtCore.pyqtSignal(str, str)

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupLayout()

    def setupLayout(self):
        label = QtGui.QLabel('Select source and destination for import:')
        self.sourceWidget = SourceWidget()
        self.destinationWidget = CategoryWidget()
        self.setEvent.connect(self.destinationWidget.setEvent)
        self.backButton = QtGui.QPushButton('Back')
        self.backButton.clicked.connect(self.previousPage)
        self.importButton = QtGui.QPushButton('Import')
        self.importButton.clicked.connect(self.importImages)

        grid = QtGui.QGridLayout()
        grid.addWidget(label, 0, 0, 1, 2)
        grid.addWidget(self.sourceWidget, 1, 0)
        grid.addWidget(self.destinationWidget, 1, 1)
        grid.addWidget(self.backButton, 3, 0)
        grid.addWidget(self.importButton, 3, 1)
        grid.setContentsMargins(0, 0, 0, 0)

        self.setLayout(grid)

    def importImages(self):
        source = self.sourceWidget.getSelectedPath()
        destination = self.destinationWidget.getSelectedPath()
        if source and destination:
            self.setSourceDest.emit(source, destination)
            self.nextPage.emit()
        else:
            title = 'Select source and destination'
            message = 'Please select a source and destination'
            message += ' for image import.'
            QtGui.QMessageBox.information(self, title, message)
