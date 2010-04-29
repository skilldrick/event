from PyQt4 import QtCore, QtGui

from featurebroker import *
import functions

class EventsPage(QtGui.QWidget):
    config = RequiredFeature('Config', hasMethods('eventsDir'))
    eventList = RequiredFeature('EventList')
    nextPage = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupLayout()
        self.eventErrorDialog = QtGui.QErrorMessage(self)
        
    def setupLayout(self):
        numberOfEvents = self.eventList.numberOfEvents()
        self.eventsCountLabel = QtGui.QLabel()
        self.listWidget = QtGui.QListWidget()
        self.makeList()
        
        newEventButton = QtGui.QPushButton('New Event')
        newEventButton.clicked.connect(self.getEvent)
        refreshButton = QtGui.QPushButton('Refresh')
        refreshButton.clicked.connect(self.refreshEvents)
        self.removeEventButton = QtGui.QPushButton('Remove Event')
        self.removeEventButton.clicked.connect(self.removeEvent)
        self.continueButton = QtGui.QPushButton('Continue')
        self.continueButton.clicked.connect(self.nextPage)
        self.listWidget.currentRowChanged.connect(self.rowChanged)
        self.disableButtons()
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.eventsCountLabel)
        vbox.addWidget(self.listWidget)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(newEventButton)
        hbox.addWidget(refreshButton)
        hbox.addWidget(self.removeEventButton)
        hbox.addWidget(self.continueButton)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def rowChanged(self, row):
        if row == -1:
            self.disableButtons()
        else:
            self.listWidget.setCurrentRow(row)
            self.enableButtons()

    def enableButtons(self):
        self.removeEventButton.setEnabled(True)
        self.continueButton.setEnabled(True)

    def disableButtons(self):
        self.removeEventButton.setEnabled(False)
        self.continueButton.setEnabled(False)
        
    def makeList(self):
        self.listWidget.clear()
        for i, event in enumerate(self.eventList.getEvents()):
            item = QtGui.QListWidgetItem()
            item.setText(event)
            self.listWidget.insertItem(i, item)
        self.eventsCountLabel.setText("{number} events in '{eventsDir}'".format(number=self.eventList.numberOfEvents(),
                                                                                eventsDir=self.config.eventsDir()))
        
    def getEvent(self):
        qtText = QtGui.QInputDialog.getText(self, 'New event',
                                          'Event name:')
        text = functions.QStringToPythonString(qtText)
        if len(text) > 0:
            self.addEvent(functions.QStringToPythonString(text))

    def addEvent(self, event):
        try:
            self.eventList.addEvent(event)
            self.makeList()
            self.repaint()
        except EventError:
            self.eventErrorDialog.showMessage('Couldn\'t create {event}'.format(event=event))

    def removeEvent(self):
        text = self.listWidget.currentItem().text()
        event = str(text)
        try:
            self.eventList.removeEvent(event)
            self.makeList()
            self.repaint()
        except EventError:
            self.eventErrorDialog.showMessage('Couldn\'t remove {event}: not empty or directory does not exist'.format(event=event))

    def refreshEvents(self):
        self.makeList()


