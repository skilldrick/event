from PyQt4 import QtCore, QtGui

from featurebroker import *
import functions
from categories import Categories

class Shared(QtGui.QWidget):
    config = RequiredFeature('Config', hasMethods('eventsDir'))
    itemStrings = {'singularCaps': 'Item',
                  'singularLower': 'item',
                  'pluralCaps': 'Items',
                  'pluralLower': 'items',
                  }

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)

    def getItem(self):
        title = 'New {item}'.format(item=self.itemStrings['singularLower'])
        body = '{item} name:'.format(item=self.itemStrings['singularCaps'])
        qtText = QtGui.QInputDialog.getText(self, title, body)
        text = functions.QStringToPythonString(qtText)
        if len(text) > 0:
            self.addItem(text)

    def addItem(self, itemName):
        self.model.addItem(self.eventsDirIndex, itemName)

    def removeItem(self):
        selectedIndex = self.getSelectedIndex()
        if selectedIndex:
            if not self.model.removeItem(selectedIndex):
                self.itemRemoveFailed()

    def itemRemoveFailed(self):
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
    
