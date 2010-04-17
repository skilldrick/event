import sys
from PyQt4 import QtCore, QtGui

class Widget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        #self.model = QtGui.QDirModel()
        self.model = QtGui.QFileSystemModel()
        currentPath = QtCore.QDir.currentPath()
        root = '/'
        self.model.setRootPath(currentPath)
        parentIndex = self.model.index(currentPath)

        rows = self.model.rowCount(parentIndex)
        print rows
        print 'Has children?', self.model.hasChildren(parentIndex)

        treeView = QtGui.QTreeView()
        treeView.setModel(self.model)
        treeView.setRootIndex(parentIndex)
        self.parentIndex = parentIndex

        treeView.clicked.connect(self.printRowCount)
        self.timer = QtCore.QTimer(self)
        self.timer.singleShot(1, self.printRowCount)
        
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(treeView)
        self.setLayout(vbox)

    def printRowCount(self):
        print 'rowCount', self.model.rowCount(self.parentIndex)


def main():
    app = QtGui.QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
