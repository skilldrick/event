from PyQt4 import QtCore, QtGui

from featurebroker import *
import functions
from categories import Categories
from shared import Shared

class EventsPage(Shared):
    config = RequiredFeature('Config', hasMethods('eventsDir'))
    nextPage = QtCore.pyqtSignal()
    itemStrings = {'singularCaps': 'Event',
                   'singularLower': 'event',
                   'pluralCaps': 'Events',
                   'pluralLower': 'events',
                   }

    def __init__(self, parent=None):
        Shared.__init__(self, parent)
        self.setupLayout()
        self.eventErrorDialog = QtGui.QErrorMessage(self)
        
    def setupLayout(self):
        self.view = QtGui.QListView()
        self.model = Categories(self)
        self.view.setModel(self.model)
        self.model.setRootPath(self.config.eventsDir())
        self.eventsDirIndex = self.model.index(self.config.eventsDir())
        self.view.setRootIndex(self.eventsDirIndex)
        self.eventsCountLabel = QtGui.QLabel()
        newEventButton = QtGui.QPushButton('New Event')
        newEventButton.clicked.connect(self.getItem)
        self.removeEventButton = QtGui.QPushButton('Remove Event')
        self.removeEventButton.clicked.connect(self.removeItem)
        self.continueButton = QtGui.QPushButton('Continue')
        self.continueButton.clicked.connect(self.nextPage)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.eventsCountLabel)
        vbox.addWidget(self.view)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(newEventButton)
        hbox.addWidget(self.removeEventButton)
        hbox.addWidget(self.continueButton)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def enableButtons(self):
        self.removeEventButton.setEnabled(True)
        self.continueButton.setEnabled(True)

    def disableButtons(self):
        self.removeEventButton.setEnabled(False)
        self.continueButton.setEnabled(False)
        

