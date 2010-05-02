from PyQt4 import QtCore, QtGui

from featurebroker import *
from config import Config
from categories import Categories
from shared import Shared
import functions

class CategoriesPage(Shared):
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
        self.view = QtGui.QTreeView()
        self.addCatButton = QtGui.QPushButton('Add category')
        self.addCatButton.clicked.connect(self.getItem)
        self.addCatButton.setEnabled(False)
        self.removeCatButton = QtGui.QPushButton('Remove category')
        self.removeCatButton.clicked.connect(self.removeItem)
        self.removeCatButton.setEnabled(False)

        self.currentEventLabel = QtGui.QLabel('No event set')
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.currentEventLabel)
        vbox.addWidget(self.view)
p        vbox.addWidget(self.removeCatButton)
        vbox.addWidget(self.addCatButton)
        self.setLayout(vbox)
        self.setEvent('rugby')
        """setEvent should be called from eventspage.py
        when next is pressed.
        """

    def setEvent(self, eventName):
        self.model = Categories(self)
        self.currentEventLabel.setText('Categories in ' + eventName)
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
        if selectedIndex:
            if not self.model.addItem(selectedIndex, categoryName):
                print 'addItem failed'

