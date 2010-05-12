from PyQt4 import QtCore, QtGui

from featurebroker import *
import functions
from .shared import Shared
from .categorywidget import CategoryWidget

class SourceWidget(Shared):
    model = RequiredFeature('SourceList')
    
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
        #get name, then path.
        #if name is len() == 0, then don't bother getting path.
        #qtText = QtGui.QInputDialog.getText(self, title, body)[0]
        #text = str(qtText)
        #text = str(qtText)
        #if len(text) > 0:
            #self.addItem(text)

        pass

    def addItem(self):
        #self.model.addItem(item)
        pass

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

        grid = QtGui.QGridLayout()
        grid.addWidget(label, 0, 0, 1, 2)
        grid.addWidget(self.sourceWidget, 1, 0)
        grid.addWidget(self.destinationWidget, 1, 1)
        grid.addWidget(self.backButton, 3, 0)

        self.setLayout(grid)

