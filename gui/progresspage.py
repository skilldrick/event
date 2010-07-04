from PyQt4 import QtCore, QtGui

from featurebroker import *


class ProgressPage(QtGui.QWidget):


    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupLayout()

    def setupLayout(self):
        label = QtGui.QLabel('Loading ...')
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(label)
        self.setLayout(vbox)
