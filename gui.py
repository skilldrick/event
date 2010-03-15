import sys
from PyQt4 import QtCore, QtGui

import Image
import ImageQt

    

class MyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('My Widget!')

        
        im = Image.open('kitten.jpg')
        print im.format
        newImage = ImageQt.ImageQt(im)
        pixmap = QtGui.QPixmap.fromImage(newImage)
        label = QtGui.QLabel('Hello', self)
        label.setPixmap(pixmap)

        quit = QtGui.QPushButton('Close', self)
        self.connect(quit, QtCore.SIGNAL('clicked()'),
                     QtGui.qApp, QtCore.SLOT('quit()'))


app = QtGui.QApplication(sys.argv)
myWidget = MyWidget()
myWidget.show()


sys.exit(app.exec_())
