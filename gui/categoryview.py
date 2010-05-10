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


class CategoryView(DeselectableTreeView):
    #should this inherit Shared or DeselectableTreeView?
    def __init__(self, parent=None):
        DeselectableTreeView.__init__(self, parent)
        
    def setEvent(self, eventName):
        pass
    
