from PyQt4 import QtCore, QtGui

from featurebroker import *

class CategoriesPage(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
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
        items = [QtGui.QTreeWidgetItem(),
                 QtGui.QTreeWidgetItem(),
                 ]
        subitem = QtGui.QTreeWidgetItem()
        subitem.setText(0, 'yo')
        items[0].setText(0, 'hello')
        items[0].insertChild(0, subitem)
        items[1].setText(0, 'hi')
        self.tree.insertTopLevelItems(0, items)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.tree)
        self.setLayout(vbox)
        
        
