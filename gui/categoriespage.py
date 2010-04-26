from PyQt4 import QtCore, QtGui

from featurebroker import *
from categories import Categories

class CategoriesPage(QtGui.QWidget):
    categories = RequiredFeature('Categories')

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupLayout()

    def setupLayout(self):
        self.model = Categories(self)
        currentPath = QtCore.QDir.currentPath()
        self.model.setRootPath(currentPath)
        currentPathIndex = self.model.index(currentPath)
        self.view = QtGui.QTreeView()
        self.view.setModel(self.model)
        self.view.setRootIndex(currentPathIndex)
        for col in range(1, 4):
            self.view.hideColumn(col)
        self.view.setHeaderHidden(True)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.view)
        self.setLayout(vbox)

