import sys
from PyQt4 import QtCore, QtGui
import Image
import ImageQt
import optparse
import unittest

from config import Config
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
    config = RequiredFeature('Config', HasMethods('eventsDir'))
    filesystem = RequiredFeature('Filesystem')
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        eventsDir = self.config.eventsDir()
        dirs = self.filesystem.listDirs(eventsDir)
        numberOfDirs = len(dirs)
        if numberOfDirs == 0:
            label = QtGui.QLabel("No events in '{eventsDir}'".format(eventsDir=eventsDir))
        else:
            labelText = ', '.join(dirs)
            label = QtGui.QLabel(labelText)
        newEventButton = QtGui.QPushButton('New Event')
        newEventButton.clicked.connect(self.getEvent)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(newEventButton)
        self.setLayout(vbox)

    def getEvent(self):
        text = QtGui.QInputDialog.getText(self, 'New event',
                                          'Event name:')
        self.addEvent(QStringToPythonString(text))

    def addEvent(self, event):
        try:
            self.filesystem.makeDir([self.config.eventsDir(), event])
        except IOError:
            print 'Couldn\'t create {event}'.format(event=event)
        
        


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
    features.Provide('Config', Config)
    features.Provide('Filesystem', Filesystem)
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
