import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
from xml.parsers.expat import ExpatError
import unittest

from filesystem import Filesystem

class ConfigFile:
    _configPath = 'config.xml'

    initSources = [ #these are used to initialise configfile
        {'name':'Memory card', 'location':'D:/'},
        {'name':'Temp folder', 'location':'C:/Photos'}
        ]
    initThumbSize = 200

    def configPath(self):
        return self._configPath

    def setConfigPath(self, path):
        self._configPath = path

    def __init__(self, path=None):
        if path:
            self.setConfigPath(path)
        try:
            self.dom = MD.parse(self.configPath())
        except (IOError, ExpatError): # No config file so initialise new one
            #print 'Error reading/parsing', self.configPath()
            #print 'Initialising new config file:', self.configPath()
            self.initConfigXml()
            self.dom = MD.parse(self.configPath())

    def addSubElement(self, parent, name, contents=None):
        newElement = self.dom.createElement(name)
        parent.appendChild(newElement)
        if not contents == None:
            contents = str(contents)
            text = self.dom.createTextNode(contents)
            newElement.appendChild(text)
        return newElement

    def addSource(self, path, name):
        sourceList = self.dom.getElementsByTagName('sourcelist')[0]
        newSource = self.addSubElement(sourceList, 'item')
        self.addSubElement(newSource, 'name', name)
        self.addSubElement(newSource, 'location', path)
        self.writeDomToFile()

    def removeSource(self, name):
        success = True
        sourceList = self.dom.getElementsByTagName('sourcelist')[0]
        for item in sourceList.childNodes:
            itemName = item.getElementsByTagName('name')[0].\
                firstChild.nodeValue
            if name == itemName:
                sourceList.removeChild(item)
                break
        else: #loop ran to completion without finding item
            success = False

        self.writeDomToFile()
        return success

    def getData(self, parentTag, childTag):
        ret = []
        for item in self.dom.getElementsByTagName(parentTag)[0].childNodes:
            childNode = item.getElementsByTagName(childTag)[0]
            ret.append(childNode.firstChild.toxml())
        return ret

    def getProperty(self, name):
        try:
            item = self.dom.getElementsByTagName(name)[0].firstChild
        except IndexError:
            return None
        text = unicode(item.toxml())
        if text.isnumeric():
            return int(text)
        else:
            return text

    def setProperty(self, name, value):
        success = True
        root = self.dom.childNodes[0]
        try:
            node = self.dom.getElementsByTagName(name)[0]
            root.removeChild(node)
        except IndexError:
            pass
        self.addSubElement(root, name, value)
        return success

    def writeDomToFile(self):
        file = open(self.configPath(), 'w')
        root = self.dom.childNodes[0]
        root.writexml(file)
        file.close()
        #use the code from initConfigXml(), then replace it with this

    def initConfigXml(self):
        self.dom = MD.parseString('<config />')
        root = self.dom.childNodes[0]

        #Set up list of sources using member initSources
        sourcelist = self.addSubElement(root, 'sourcelist')
        for item in self.initSources:
            newItem = self.addSubElement(sourcelist, 'item')
            self.addSubElement(newItem, 'name', item['name'])
            self.addSubElement(newItem, 'location', item['location'])

        #This is the thumbnail size used in importpage
        self.addSubElement(root, 'thumbsize', self.initThumbSize)

        self.writeDomToFile()

class ConfigFileTests(unittest.TestCase):
    testConfigPath = 'testconfig.xml'

    def setUp(self):
        self.configFile = ConfigFile(self.testConfigPath)

    def tearDown(self):
        Filesystem().removeFile(self.testConfigPath)
        
    def assertListsEqual(self, list1, list2):
        for item1, item2 in zip(list1, list2):
            self.assertEqual(item1, item2)

    def getListFromInitSources(self, key):
        #initSources is a list of sources for initialising
        #the config file. This function produces a list of
        #either the name or the location of each source.
        ret = []
        for item in self.configFile.initSources:
            ret.append(item[key])
        return ret

    def testGetNames(self):
        sourceNames = self.configFile.getData('sourcelist', 'name')
        self.assertListsEqual(sourceNames,
                              self.getListFromInitSources('name'))

    def testGetLocations(self):
        locations = self.configFile.getData('sourcelist', 'location')
        self.assertListsEqual(locations,
                              self.getListFromInitSources('location'))

    def testAddSource(self):
        self.configFile.addSource('blah/blah', 'blah')
        self.assertTrue('blah' in self.configFile.getData('sourcelist', 'name'))

    def testRemoveSource(self):
        self.configFile.addSource('myah/hah', 'myahhah')
        self.configFile.removeSource('myahhah')
        self.assertFalse('myahhah' in self.configFile.getData('sourcelist', 'name'))

    def testGetProperty(self):
        self.assertEqual(self.configFile.initThumbSize,
                         self.configFile.getProperty('thumbsize'))

    def testGetMissingProperty(self):
        self.assertEqual(self.configFile.getProperty('dsagsadg'),
                         None)

    def testSetNewProperty(self):
        testName = 'blahblah'
        testValue = 100
        self.configFile.setProperty(testName, testValue)
        self.assertEqual(self.configFile.getProperty(testName),
                         testValue)

    def testSetExistingProperty(self):
        testName = 'thumbsize'
        testValue = 500
        self.configFile.setProperty(testName, testValue)
        self.assertEqual(self.configFile.getProperty(testName),
                         testValue)
        

def suite():
    testSuite = unittest.makeSuite(ConfigFileTests)
    return testSuite

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())


class Config:
    _eventsDir = 'events'
    
    def __init__(self):
        self.configFile = ConfigFile()

    def eventsDir(self):
        return self._eventsDir

    def setEvent(self, event):
        self._event = event

    def getEvent(self):
        return self._event

    def addSource(self, path, name):
        self.configFile.addSource(path, name)

    def removeSource(self, name):
        return self.configFile.removeSource(name)

    def getSourceNameList(self):
        return self.configFile.getData('sourcelist', 'name')

    def getSourceLocationList(self):
        return self.configFile.getData('sourcelist', 'location')

    def getProperty(self, name):
        return self.configFile.getProperty(name)

    def setProperty(self, name, value):
        self.configFile.setProperty(name, value)
