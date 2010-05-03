from PyQt4 import QtCore

def QStringToPythonString(qString):
    assert False, 'Obsolete function, use str(qString[0])'
    assert isinstance(qString[0], QtCore.QString)
    return str(qString[0])

