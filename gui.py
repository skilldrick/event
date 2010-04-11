import sys
from PyQt4 import QtCore, QtGui
import Image
import ImageQt
import optparse
import unittest

from config import Config
from eventlist import EventList, EventError
from filesystem import Filesystem
from featurebroker import *


def QStringToPythonString(QString):
    return str(QString[0].toAscii())


class Stacked(QtGui.QStackedWidget):
    def __init__(self, parent=None):
        QtGui.QStackedWidget.__init__(self, parent)
        self.widget1 = EventsPage()
        self.widget2 = MyWidget('imagesdir/kitten.jpg')
        self.widget3 = MyWidget('imagesdir/kitten-portrait.jpg')
        self.addWidget(self.widget1)
        self.addWidget(self.widget2)
        self.addWidget(self.widget3)

    def nextPage(self):
        self.setCurrentIndex(self.currentIndex() + 1)

    def previousPage(self):
        self.setCurrentIndex(self.currentIndex() - 1)


class EventsPage(QtGui.QWidget):
    config = RequiredFeature('Config', hasMethods('eventsDir'))
    eventList = RequiredFeature('EventList')

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.listWidget = QtGui.QListWidget()
        self.setupLayout()
        
    def setupLayout(self):
        numberOfEvents = self.eventList.numberOfEvents()
        if numberOfEvents > 0:
            label = QtGui.QLabel("{number} events in '{eventsDir}'".format(number=numberOfEvents,
                                                                           eventsDir=self.config.eventsDir()))
            self.makeList()
        else:
            label = QtGui.QLabel("No events in '{eventsDir}'".format(eventsDir=self.config.eventsDir()))
        newEventButton = QtGui.QPushButton('New Event')
        newEventButton.clicked.connect(self.getEvent)
        refreshButton = QtGui.QPushButton('Refresh')
        refreshButton.clicked.connect(self.refreshEvents)
        removeEventButton = QtGui.QPushButton('Remove Event')
        removeEventButton.clicked.connect(self.removeEvent)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(label)
        if numberOfEvents > 0:
            vbox.addWidget(self.listWidget)
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(newEventButton)
        hbox.addWidget(refreshButton)
        hbox.addWidget(removeEventButton)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        
    def makeList(self):
        self.listWidget.clear()
        for i, event in enumerate(self.eventList.getEvents()):
            item = QtGui.QListWidgetItem()
            item.setText(event)
            self.listWidget.insertItem(i, item)
        
    def getEvent(self):
        text = QtGui.QInputDialog.getText(self, 'New event',
                                          'Event name:')
        self.addEvent(QStringToPythonString(text))

    def addEvent(self, event):
        try:
            self.eventList.addEvent(event)
            self.makeList()
            self.repaint()
        except EventError:
            print 'Couldn\'t create {event}'.format(event=event)

    def removeEvent(self):
        text = QtGui.QInputDialog.getText(self, 'Remove event',
                                          'Event name:')
        event = QStringToPythonString(text)

        try:
            self.eventList.removeEvent(event)
            self.makeList()
            self.repaint()
        except EventError:
            print 'Couldn\'t remove {event}: not empty'.format(event=event)

    def refreshEvents(self):
        self.makeList()
        #this isn't done yet, because it needs to change the layout if there are no events.
        #would it be easier to have two widgets?


class MasterWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('My Widget!')
        layout = QtGui.QVBoxLayout()
        self.stacked = Stacked(self)

        self.previous = QtGui.QPushButton('Previous')
        self.previous.clicked.connect(self.stacked.previousPage)
        self.next = QtGui.QPushButton('Next')
        self.next.clicked.connect(self.stacked.nextPage)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.previous)
        hbox.addWidget(self.next)
        
        layout.addWidget(self.stacked)        
        layout.addLayout(hbox)
        self.setLayout(layout)


class MyWidget(QtGui.QWidget):
    def __init__(self, imagePath, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 400, 293)
        self.setWindowTitle('My Widget!')

        pixmap = self.convertImage(Image.open(imagePath))

        label = QtGui.QLabel('', self)
        label.setPixmap(pixmap)

    def convertImage(self, image):
        """Takes a PIL image and returns a QtPixmap"""
        QtImage1 = ImageQt.ImageQt(image)
        QtImage2 = QtGui.QImage(QtImage1)
        pixmap = QtGui.QPixmap.fromImage(QtImage2)
        return pixmap


def main():
    app = QtGui.QApplication(sys.argv)
    features.provide('Config', Config)
    features.provide('EventList', EventList)
    features.provide('Filesystem', Filesystem)
    masterWidget = MasterWidget()
    masterWidget.show()
    sys.exit(app.exec_())


def test():
    print 'No tests set up'


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("-t", "--test", action="store_true")
    options, args = parser.parse_args()
    del sys.argv[1:] #This needs to be done to make sure unittest doesn't break
    if options.test:
        test()
    else:
        main()
