from PyQt4 import QtCore, QtGui

from featurebroker import *
import functions
from directorymodel import DirectoryModel
from .shared import Shared

class EventsPage(Shared):
    config = RequiredFeature('Config')
    filesystem = RequiredFeature('Filesystem')
    setEvent = QtCore.pyqtSignal(str)
    nextPage = QtCore.pyqtSignal()
    itemStrings = {'singularCaps': 'Event',
                   'singularLower': 'event',
                   'pluralCaps': 'Events',
                   'pluralLower': 'events',
                   }

    def __init__(self, parent=None):
        Shared.__init__(self, parent)
        self.timer = QtCore.QTimer(self)
        self.setupLayout()
        self.updateLabelTimer()
        self.eventErrorDialog = QtGui.QErrorMessage(self)
        
    def setupLayout(self):
        self.view = QtGui.QListView()
        self.model = DirectoryModel(self)
        self.model.modelChanged.connect(self.updateLabelTimer)
        self.view.setModel(self.model)
        self.setRoot()
        self.eventsCountLabel = QtGui.QLabel()
        self.eventsCountLabel.linkActivated.connect(self.changeEventsDir)
        newEventButton = QtGui.QPushButton('New Event')
        newEventButton.clicked.connect(self.getItem)
        self.removeEventButton = QtGui.QPushButton('Remove Event')
        self.removeEventButton.clicked.connect(self.removeItem)
        self.continueButton = QtGui.QPushButton('Continue')
        self.continueButton.clicked.connect(self.sendIndexToNextPage)
        self.view.doubleClicked.connect(self.sendIndexToNextPage)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.eventsCountLabel)
        vbox.addWidget(self.view)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(newEventButton)
        hbox.addWidget(self.removeEventButton)
        hbox.addWidget(self.continueButton)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def setRoot(self, eventsDir=None):
        if not eventsDir:
            eventsDir = self.config.getEventsDir()
        self.model.setRootPath(eventsDir)
        self.eventsDirIndex = self.model.index(eventsDir)
        self.view.setRootIndex(self.eventsDirIndex)

    def updateLabelTimer(self):
        #updateLabel() has to happen in a different thread:
        self.timer.singleShot(0, self.updateLabel)
        #If it fires too soon, 100ms should be enough:
        self.timer.singleShot(100, self.updateLabel)

    def updateLabel(self):
        index = self.view.rootIndex()
        count = self.model.rowCount(index)
        if count > 1 or count == 0:
            s = 's'
        else:
            s = ''
        labelText = "{count} event{s} in \
            <a href='change'>{eventsDir}</a>".format(
            count=count, s=s, eventsDir=self.config.getEventsDir())
        self.eventsCountLabel.setText(labelText)

    def changeEventsDir(self):
        title = 'Choose new events directory'
        path = QtGui.QFileDialog.getExistingDirectory(self, title)
        self.config.setEventsDir(path)
        self.setRoot(path)
        self.updateLabel()

    def sendIndexToNextPage(self):
        eventName = self.getSelectedName()
        if eventName:
            self.setEvent.emit(eventName)
            self.nextPage.emit()
        else:
            print 'No event selected'

    def enableButtons(self):
        self.removeEventButton.setEnabled(True)
        self.continueButton.setEnabled(True)

    def disableButtons(self):
        self.removeEventButton.setEnabled(False)
        self.continueButton.setEnabled(False)
        

