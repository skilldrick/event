from PyQt4 import QtCore, QtGui

from featurebroker import *
import functions
from .shared import Shared
from .categorywidget import CategoryWidget

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
        self.setLayout(vbox)

    def getItem(self):
        #qt prefix means qString
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

    def printLocation(self):
        index = self.getSelectedIndex()
        print self.model.data(index, QtCore.Qt.UserRole)
        

class SourceDestPage(QtGui.QWidget):
    config = RequiredFeature('Config')
    sourceList = RequiredFeature('SourceList')
    previousPage = QtCore.pyqtSignal()
    nextPage = QtCore.pyqtSignal()
    setEvent = QtCore.pyqtSignal(str)

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

        self.setLayout(grid)

    def importImages(self):
        pass
