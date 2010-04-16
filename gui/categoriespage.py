from PyQt4 import QtCore, QtGui

from featurebroker import *
from categories import Categories

class CategoriesPage(QtGui.QWidget):
    categories = RequiredFeature('Categories')

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        categoriesTree = self.categories.getTree()
        self.setupLayout()

    def setupLayout(self):
        """
        self.model = QtGui.QFileSystemModel(self)
        self.model.setRootPath('~/Programming/Python/event/events')
        self.view = QtGui.QTreeView()
        self.view.setModel(self.model)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.view)
        self.setLayout(vbox)
        """

        self.tree = QtGui.QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabel('Category')

        topLevelText = ['Boys', 'Girls']
        topLevelItems = self.makeListOfItems(topLevelText)
        boys = self.makeListOfItems(['Under 8s', 'Under 9s', 'Under 10s'])
        topLevelItems[0].insertChildren(0, boys)
        girls = self.makeListOfItems(['Under 10s', 'Over 10s'])
        topLevelItems[1].insertChildren(0, girls)
        root = QtGui.QTreeWidgetItem()
        root.setText(0, 'Rugby')
        root.insertChildren(0, topLevelItems)

        """
        subitem = QtGui.QTreeWidgetItem()
        subitem.setText(0, 'yo')
        topLevelItems[0].insertChild(0, subitem)
        """
        """
        root = QtGui.QTreeWidgetItem()
        root.setText(0, 'Rugby')
        """
        self.tree.insertTopLevelItem(0, root)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.tree)
        self.setLayout(vbox)

    def convertTree(self):
         pass


        
    def makeListOfItems(self, listOfNames):
        listOfItems = []
        for name in listOfNames:
            listOfItems.append(self.makeItemFromName(name))
        return listOfItems

    def makeItemFromName(self, name):
        item = QtGui.QTreeWidgetItem()
        item.setText(0, name)
        return item
    
