from PyQt4 import QtCore, QtGui

from featurebroker import *
import functions
from .shared import Shared
from .categorywidget import CategoryWidget

class SourceDestWidget(Shared):
    def __init__(self, parent=None):
        Shared.__init__(self, parent)
        self.setupLayout()

    def setupLayout(self):
        self.view = QtGui.QListView()
        self.view.setModel(self.model)
        temp = QtGui.QPushButton('temp')
        temp.clicked.connect(self.printLocation)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.view)
        vbox.addWidget(temp)

        self.setLayout(vbox)

    def printLocation(self):
        index = self.getSelectedIndex()
        print self.model.data(index, QtCore.Qt.UserRole)
        

class SourceWidget(SourceDestWidget):
    model = RequiredFeature('SourceList')

    def __init__(self, parent=None):
        SourceDestWidget.__init__(self)


class DestinationWidget(CategoryWidget):
    """
    At the moment DestinationWidget is just a CategoryWidget.
    Is it necessary to have two CategoryWidgets? Could we
    combine the function of categoriespage with that of
    sourcedestpage? Ask Kazz.
    """
    def __init__(self, parent=None):
        CategoryWidget.__init__(self)
    

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
        self.destinationWidget = DestinationWidget()
        self.setEvent.connect(self.destinationWidget.setEvent)
        self.backButton = QtGui.QPushButton('Back')
        self.backButton.clicked.connect(self.previousPage)

        grid = QtGui.QGridLayout()
        grid.addWidget(label, 0, 0, 1, 2)
        grid.addWidget(self.sourceWidget, 1, 0)
        grid.addWidget(self.destinationWidget, 1, 1)
        grid.addWidget(self.backButton, 3, 0)

        self.setLayout(grid)

