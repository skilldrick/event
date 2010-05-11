from PyQt4 import QtCore, QtGui

from featurebroker import *
from config import Config
from directorymodel import DirectoryModel
from shared import Shared
import functions
from categorywidget import CategoryWidget


class DeselectableTreeView(QtGui.QTreeView):
    def mousePressEvent(self, event):
        """When the TreeView is clicked, the selection is cleared.
        If an item is clicked, QTreeView.mousePressEvent() selects it"""
        self.clearSelection()
        QtGui.QTreeView.mousePressEvent(self, event)


class CategoriesPage(QtGui.QWidget):
    previousPage = QtCore.pyqtSignal()
    nextPage = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupLayout()

    def setupLayout(self):
        self.categoryWidget = CategoryWidget()
        self.backButton = QtGui.QPushButton('Back')
        self.backButton.clicked.connect(self.previousPage)
        self.addCatButton = QtGui.QPushButton('Add category')
        self.addCatButton.clicked.connect(self.categoryWidget.getItem)
        self.removeCatButton = QtGui.QPushButton('Remove category')
        self.removeCatButton.clicked.connect(self.categoryWidget.removeItem)
        self.continueButton = QtGui.QPushButton('Continue')
        self.continueButton.clicked.connect(self.nextPage)

        self.currentEventLabel = QtGui.QLabel('No event set')
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.currentEventLabel)
        vbox.addWidget(self.categoryWidget)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.backButton)
        hbox.addWidget(self.removeCatButton)
        hbox.addWidget(self.addCatButton)
        hbox.addWidget(self.continueButton)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def setEvent(self, eventName):
        eventName = str(eventName)
        self.currentEventLabel.setText('Set up categories in '
                                       + eventName + ':')
        self.addCatButton.setEnabled(True)
        self.removeCatButton.setEnabled(True)
        self.categoryWidget.setEvent(eventName)

