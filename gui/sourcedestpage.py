from PyQt4 import QtCore, QtGui

from featurebroker import *
import functions

class SourceDestPage(QtGui.QWidget):
    config = RequiredFeature('Config')
    sourceList = RequiredFeature('SourceList')
    previousPage = QtCore.pyqtSignal()
    nextPage = QtCore.pyqtSignal()


    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupLayout()

    def setupLayout(self):
        label = QtGui.QLabel('Select source and destination for import:')
        self.sourceView = QtGui.QListView()
        self.sourceView.setModel(self.sourceList)
        self.destinationView = QtGui.QListView()
        self.backButton = QtGui.QPushButton('Back')
        self.backButton.clicked.connect(self.previousPage)

        grid = QtGui.QGridLayout()
        grid.addWidget(label, 0, 0, 1, 2)
        grid.addWidget(self.sourceView, 1, 0)
        grid.addWidget(self.destinationView, 1, 1)
        grid.addWidget(self.backButton, 3, 0)
        
        self.setLayout(grid)
