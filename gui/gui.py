import sys
from PyQt4 import QtCore, QtGui
import Image
import ImageQt
import optparse
import unittest

from config import Config
from eventlist import EventList, EventError
from categories import Categories
from filesystem import Filesystem
from sourcelist import SourceList
from importer import Importer
from featurebroker import *
from .eventspage import EventsPage
from .sourcedestpage import SourceDestPage
from .importpage import ImportPage


class Stacked(QtGui.QStackedWidget):
    def __init__(self, parent=None):
        QtGui.QStackedWidget.__init__(self, parent)
        self.widget1 = EventsPage()
        self.widget2 = SourceDestPage()
        self.widget3 = ImportPage()
        
        self.widget1.nextPage.connect(self.nextPage)
        self.widget1.setEvent.connect(self.widget2.setEvent)
        self.widget2.previousPage.connect(self.previousPage)
        self.widget2.nextPage.connect(self.nextPage)
        self.widget2.setSourceDest.connect(self.widget3.setSourceDest)
        self.addWidget(self.widget1)
        self.addWidget(self.widget2)
        self.addWidget(self.widget3)

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

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.previous)
        hbox.addWidget(self.next)
        
        vbox.addWidget(self.stacked)        
        vbox.addLayout(hbox)
        self.setLayout(vbox)


class MyWidget(QtGui.QWidget):
    def __init__(self, imagePath, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 400, 293)
        self.setWindowTitle('My Widget!')

        pixmap = QtGui.QPixmap(imagePath)
        label = QtGui.QLabel('', self)
        label.setPixmap(pixmap)


def main():
    app = QtGui.QApplication(sys.argv)
    features.provide('Config', Config)
    features.provide('EventList', EventList)
    features.provide('Filesystem', Filesystem)
    features.provide('Categories', Categories)
    features.provide('SourceList', SourceList)
    features.provide('Importer', Importer)
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
