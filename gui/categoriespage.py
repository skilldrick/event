from PyQt4 import QtCore, QtGui

from featurebroker import *
from config import Config
from directorymodel import DirectoryModel
from shared import Shared
import functions
from categoryview import CategoryView


class DeselectableTreeView(QtGui.QTreeView):
    def mousePressEvent(self, event):
        """When the TreeView is clicked, the selection is cleared.
        If an item is clicked, QTreeView.mousePressEvent() selects it"""
        self.clearSelection()
        QtGui.QTreeView.mousePressEvent(self, event)


class CategoriesPage(Shared):
    config = RequiredFeature('Config')
    filesystem = RequiredFeature('Filesystem')
    itemStrings = {'singularCaps': 'Category',
                   'singularLower': 'category',
                   'pluralCaps': 'Categories',
                   'pluralLower': 'categories',
                   }
    previousPage = QtCore.pyqtSignal()
    nextPage = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        Shared.__init__(self, parent)
        self.setupLayout()

    def setupLayout(self):
        self.view = CategoryView()
        self.backButton = QtGui.QPushButton('Back')
        self.backButton.clicked.connect(self.previousPage)
        self.addCatButton = QtGui.QPushButton('Add category')
        self.addCatButton.clicked.connect(self.getItem)
        self.removeCatButton = QtGui.QPushButton('Remove category')
        self.removeCatButton.clicked.connect(self.removeItem)
        self.continueButton = QtGui.QPushButton('Continue')
        self.continueButton.clicked.connect(self.nextPage)

        self.currentEventLabel = QtGui.QLabel('No event set')
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.currentEventLabel)
        vbox.addWidget(self.view)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.backButton)
        hbox.addWidget(self.removeCatButton)
        hbox.addWidget(self.addCatButton)
        hbox.addWidget(self.continueButton)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def setEvent(self, eventName):
        eventName = str(eventName)
        self.model = DirectoryModel(self, eventName)
        self.currentEventLabel.setText('Set up categories in ' + eventName + ':')
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
        self.addCatButton.setEnabled(True)
        self.removeCatButton.setEnabled(True)
        
    def addItem(self, categoryName):
        selectedIndex = self.getSelectedIndex()
        if not selectedIndex:
            selectedIndex = self.view.rootIndex()
        success = self.model.addItem(selectedIndex, categoryName)
        if not success:
            print 'addItem failed'


