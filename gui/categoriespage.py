from PyQt4 import QtCore, QtGui

from featurebroker import *
from config import Config
from categories import Categories
import functions

class CategoriesPage(QtGui.QWidget):
    config = RequiredFeature('Config')
    filesystem = RequiredFeature('Filesystem')
    #categories = RequiredFeature('Categories')

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupLayout()

    def setupLayout(self):
        #Need to pass self to Categories so can't use
        #straight DI. Could use a setter instead, but then
        #Categories would be left in an unconstructed state.
        self.view = QtGui.QTreeView()
        self.addCatButton = QtGui.QPushButton('Add category')
        self.addCatButton.clicked.connect(self.getCategory)
        self.addCatButton.setEnabled(False)
        self.removeCatButton = QtGui.QPushButton('Remove category')
        self.removeCatButton.clicked.connect(self.removeCategory)
        self.removeCatButton.setEnabled(False)

        self.currentEventLabel = QtGui.QLabel('No event set')
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.currentEventLabel)
        vbox.addWidget(self.view)
        vbox.addWidget(self.removeCatButton)
        vbox.addWidget(self.addCatButton)
        self.setLayout(vbox)
        self.setEvent('rugby')
        """setEvent should be called from eventspage.py
        when next is pressed. In fact, eventspage.py probably
        needs rewriting to take advantage of QFileSystemModel.
        It just needs a one-dimensional view of the events
        directory, i.e. just the top level dirs. I think
        filesystem.py was a big waste of time (but fun anyway).
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
        

    def getCategory(self):
        qtText = QtGui.QInputDialog.getText(self, 'New category',
                                          'Category name:')
        text = functions.QStringToPythonString(qtText)
        if len(text) > 0:
            self.addCategory(text)

    def addCategory(self, categoryName):
        selectedIndex = self.getSelectedIndex()
        if selectedIndex:
            if not self.model.addCategory(selectedIndex, categoryName):
                print 'addCategory failed'

    def removeCategory(self):
        selectedIndex = self.getSelectedIndex()
        if selectedIndex:
            if not self.model.removeCategory(selectedIndex):
                self.categoryRemoveFailed()
            #if remove doesn't work (directory has children)
            #then show dialog informing user of this fact

    def categoryRemoveFailed(self):
        title = 'Cannot remove category'
        message = 'This category cannot be removed.\n'
        message += 'Only empty categories can be removed.'
        QtGui.QMessageBox.warning(self, title, message)
        

    def getSelectedIndex(self):
        selectionModel = self.view.selectionModel()
        selectedRow = selectionModel.selectedIndexes()
        #this is a row of the model. Column [0] is the directory,
        #which can have children. The other columns can't
        #have children, but just contain metadata about the directory.
        if selectedRow:
            return selectedRow[0]
        else:
            return None

