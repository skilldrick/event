import sys
from PyQt4 import QtCore, QtGui
import Image
import ImageQt
import unittest

from config import Config
from eventlist import EventList, EventError
from filesystem import Filesystem
from sourcelist import SourceList
from importer import ImportList
from featurebroker import *
from .eventspage import EventsPage
from .sourcedestpage import SourceDestPage
from .importpage import ImportPage
from reset import Reset


class Stacked(QtGui.QStackedWidget):
    restart = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        QtGui.QStackedWidget.__init__(self, parent)
        self.widgets = []
        self.setupWidgets()

    def setupWidgets(self):
        self.widgets.append(EventsPage())
        self.widgets.append(SourceDestPage())
        self.widgets.append(ImportPage())
        
        self.widgets[0].nextPage.connect(self.nextPage)
        self.widgets[0].setEvent.connect(self.widgets[1].setEvent)
        self.widgets[1].previousPage.connect(self.previousPage)
        self.widgets[1].nextPage.connect(self.nextPage)
        self.widgets[1].setSourceDest.connect(self.widgets[2].setSourceDest)
        self.widgets[2].previousPage.connect(self.previousPage)
        self.widgets[2].restart.connect(self.restart)
        self.addWidget(self.widgets[0])
        self.addWidget(self.widgets[1])
        self.addWidget(self.widgets[2])
        
    def nextPage(self):
        self.setCurrentIndex(self.currentIndex() + 1)

    def previousPage(self):
        self.setCurrentIndex(self.currentIndex() - 1)

    def restart(self):
        for widget in self.widgets:
            self.removeWidget(widget)
        self.widgets = []
        self.setupWidgets()


class MasterWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('My Widget!')
        self.setupLayout()

    def setupLayout(self):
        vbox = QtGui.QVBoxLayout()
        self.stacked = Stacked(self)
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
    widget.stacked.widgets[2].setSourceDest('imagesdir', 'events/rugby/boys')
    

def test():
    provideFeatures()
    execute(modifyForTesting)


def main():
    provideFeatures()
    execute()



