from PyQt4 import QtCore, QtGui

from featurebroker import *
from config import Config
from categories import Categories

class CategoriesPage(QtGui.QWidget):
    config = RequiredFeature('Config')
    #categories = RequiredFeature('Categories')

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupLayout()

    def setupLayout(self):
        self.model = Categories(self)
        currentEventPath = 'events/rugby'
        #currentPath = QtCore.QDir.currentPath()
        currentPath = currentEventPath
        self.model.setRootPath(currentPath)
        currentPathIndex = self.model.index(currentPath)
        self.view = QtGui.QTreeView()
        self.view.setModel(self.model)
        self.view.setRootIndex(currentPathIndex)
        for col in range(1, 4):
            self.view.hideColumn(col)
        self.view.setHeaderHidden(True)

        addCatButton = QtGui.QPushButton('Add category')
        addCatButton.clicked.connect(self.addCategory)
        removeCatButton = QtGui.QPushButton('Remove category')
        removeCatButton.clicked.connect(self.removeCategory)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.view)
        vbox.addWidget(removeCatButton)
        vbox.addWidget(addCatButton)
        self.setLayout(vbox)

    def addCategory(self):
        selectedIndex = self.getSelectedIndex()
        if selectedIndex:
            self.model.addCategory(selectedIndex, 'newCat')

    def removeCategory(self):
        selectedIndex = self.getSelectedIndex()
        if selectedIndex:
            self.model.removeCategory(selectedIndex)
        

    def getSelectedIndex(self):
        selectionModel = self.view.selectionModel()
        selectedRow = selectionModel.selectedIndexes()
        if selectedRow:
            return selectedRow[0]
        else:
            return None

