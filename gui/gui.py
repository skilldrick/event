import sys
from PyQt4 import QtCore, QtGui
import Image
import ImageQt
import unittest

from config import Config
from eventlist import EventList, EventError
from filesystem import Filesystem
from sourcelist import SourceList
from importer import Importer
from featurebroker import *
from .eventspage import EventsPage
from .sourcedestpage import SourceDestPage
from .importpage import ImportPage
from .progresspage import ProgressPage
from reset import Reset


class Stacked(QtGui.QStackedWidget):
    def __init__(self, parent=None):
        QtGui.QStackedWidget.__init__(self, parent)
        self.widget1 = EventsPage()
        self.widget2 = SourceDestPage()
        self.widget3 = ImportPage()
        self.widget4 = ProgressPage()
        
        self.widget1.nextPage.connect(self.nextPage)
        self.widget1.setEvent.connect(self.widget2.setEvent)
        self.widget2.previousPage.connect(self.previousPage)
        self.widget2.nextPage.connect(self.nextPage)
        self.widget2.setSourceDest.connect(self.widget3.setSourceDest)
        self.widget3.previousPage.connect(self.previousPage)
        self.widget3.nextPage.connect(self.nextPage)
        self.addWidget(self.widget1)
        self.addWidget(self.widget2)
        self.addWidget(self.widget3)
        self.addWidget(self.widget4)

    def nextPage(self):
        self.setCurrentIndex(self.currentIndex() + 1)

    def previousPage(self):
        self.setCurrentIndex(self.currentIndex() - 1)


class MasterWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('My Widget!')
        vbox = QtGui.QVBoxLayout()
        self.stacked = Stacked(self)

        self.previous = QtGui.QPushButton('Previous')
        self.previous.clicked.connect(self.stacked.previousPage)
        self.next = QtGui.QPushButton('Next')
        self.next.clicked.connect(self.stacked.nextPage)

        vbox.addWidget(self.stacked)        
        self.setLayout(vbox)


class MyWidget(QtGui.QWidget):
    def __init__(self, imagePath, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 400, 293)
        self.setWindowTitle('My Widget!')

        pixmap = QtGui.QPixmap(imagePath)
        label = QtGui.QLabel('', self)
        label.setPixmap(pixmap)


def provideFeatures():
    features.provide('Config', Config)
    features.provide('EventList', EventList)
    features.provide('Filesystem', Filesystem)
    features.provide('SourceList', SourceList)
    features.provide('Importer', Importer)
        

def execute(callback=None):
    reset = Reset()
    reset.fill() #fill imagesdir with images
    app = QtGui.QApplication(sys.argv)
    masterWidget = MasterWidget()
    if callback:
        callback(masterWidget)
    masterWidget.show()
    exitValue = app.exec_()
    reset.empty() #delete images in imagesdir
    sys.exit(exitValue)


def modifyForTesting(widget):
    widget.stacked.setCurrentIndex(2)
    widget.stacked.widget3.setSourceDest('imagesdir', 'events/rugby/boys')
    

def test():
    provideFeatures()
    execute(modifyForTesting)


def main():
    provideFeatures()
    execute()



