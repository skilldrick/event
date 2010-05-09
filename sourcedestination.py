from PyQt4 import QtCore, QtGui

from featurebroker import *


class SourceList(QtGui.QStringListModel):
    config = RequiredFeature('Config')
    
    def __init__(self):
        QtGui.QStringListModel.__init__(self)
        self.setStringList(self.config.getSourceList())
    
