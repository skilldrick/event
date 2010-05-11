from PyQt4 import Qt, QtCore, QtGui

from featurebroker import *


class SourceList(QtGui.QStringListModel):
    config = RequiredFeature('Config')
    
    def __init__(self):
        QtGui.QStringListModel.__init__(self)
        self.setStringList(self.config.getSourceList())
        self.setLocationList(self.config.getLocationList())

    def setLocationList(self, locationList):
        self._locationList = locationList

    def locationList(self):
        return self._locationList
    
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()

        if index.row() >= len(self.stringList()):
             return QtCore.QVariant()

        if role == QtCore.Qt.DisplayRole:
            return self.stringList()[index.row()]
        elif role == QtCore.Qt.ToolTipRole or role == QtCore.Qt.UserRole:
            return self.locationList()[index.row()]
        else:
            return QtCore.QVariant()
