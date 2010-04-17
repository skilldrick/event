import sys
from PyQt4 import QtCore, QtGui

class Widget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        model = QtGui.QDirModel()
        #model.setRootPath(QtCore.QDir.currentPath())
        #print model.rootPath()
        parentIndex = model.index(QtCore.QDir.currentPath())
        print 'row:', parentIndex.row(), 'column:', parentIndex.column()
        print model.isDir(parentIndex)
        print model.data(parentIndex).toString()

        childIndex = model.index(0, 0, parentIndex)
        print model.data(childIndex).toString()

        rows = model.rowCount(parentIndex)
        print rows

        treeView = QtGui.QTreeView()
        treeView.setModel(model)
        treeView.setRootIndex(parentIndex)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(treeView)
        self.setLayout(vbox)


def main():
    app = QtGui.QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
