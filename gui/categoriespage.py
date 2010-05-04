from PyQt4 import QtCore, QtGui

from featurebroker import *
from config import Config
from directorymodel import DirectoryModel
from shared import Shared
import functions

#include root item in view? That way it is easy to add top-level
#children or lower-level children.

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
        vbox.addWidget(self.removeCatButton)
        vbox.addWidget(self.addCatButton)
        self.setLayout(vbox)

    def setEvent(self, eventName):
        eventName = str(eventName)
        self.model = DirectoryModel(self, eventName)
        self.currentEventLabel.setText('Categories in ' + eventName)
        self.view.setModel(self.model)
        for col in range(1, 4):
            self.view.hideColumn(col)
        self.view.setHeaderHidden(True)
        currentEventPath = self.filesystem.joinPath([
                self.config.eventsDir(),
                eventName,
                ])
        #currentEventPath = self.config.eventsDir() #delete this line
        #need to find some way to either insert the parent
        #or remove the siblings of the parent
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


