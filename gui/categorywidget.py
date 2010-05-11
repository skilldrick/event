from PyQt4 import QtCore, QtGui

from featurebroker import *
from config import Config
from directorymodel import DirectoryModel
from shared import Shared
import functions


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
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.view)
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



    
