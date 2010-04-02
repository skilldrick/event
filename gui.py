import sys
from PyQt4 import QtCore, QtGui
import Image
import ImageQt


class MyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 400, 293)
        self.setWindowTitle('My Widget!')


        PilImage = Image.open('kitten.jpg')
        pixmap = self.convertImage(PilImage)
        pixmap2 = self.convertImage(Image.open('imagesdir/DSC_0015.JPG'))
        label = QtGui.QLabel('', self)
        label.setPixmap(pixmap2)

    def convertImage(self, image):
        """Takes a PIL image and returns a QtPixmap"""
        QtImage1 = ImageQt.ImageQt(image)
        QtImage2 = QtGui.QImage(QtImage1)
        pixmap = QtGui.QPixmap.fromImage(QtImage2)
        return pixmap



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myWidget = MyWidget()
    myWidget.show()

    sys.exit(app.exec_())
