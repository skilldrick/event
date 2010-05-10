import xml.etree.ElementTree as ET
import xml.dom.minidom as MD

class ConfigFile:
    _configPath = 'config.xml'
    
    def configPath(self):
        return self._configPath

    def __init__(self):
        try:
            self.dom = MD.parse(self.configPath())
        except IOError: # No config file so initialise new one
            self.initConfigXml()
            self.dom = MD.parse(self.configPath())

    def removeItem(self):
        items = self.dom.getElementsByTagName('item')
        sourcelist = self.dom.getElementsByTagName('sourcelist')[0]
        print self.dom.toprettyxml()
        sourcelist.removeChild(items[0])
        print self.dom.toprettyxml()

    def addSubElement(self, parent, name, contents=None):
        newElement = self.dom.createElement(name)
        parent.appendChild(newElement)
        if not contents == None:
            text = self.dom.createTextNode(contents)
            newElement.appendChild(text)
        return newElement

    def getData(self, parentTag, childTag):
        ret = []
        for item in self.dom.getElementsByTagName(parentTag)[0].childNodes:
            childNode = item.getElementsByTagName(childTag)[0]
            ret.append(childNode.firstChild.toxml())
        return ret

    def initConfigXml(self):
        self.dom = MD.parseString('<config />')
        root = self.dom.childNodes[0]
        sourcelist = self.addSubElement(root, 'sourcelist')

        sources = [
            {'name':'Memory card', 'location':'D:/'},
            {'name':'Temp folder', 'location':'C:/Photos'}
            ]

        for item in sources:
            newItem = self.addSubElement(sourcelist, 'item')
            self.addSubElement(newItem, 'name', item['name'])
            self.addSubElement(newItem, 'location', item['location'])

        file = open(self.configPath(), 'w')
        root.writexml(file)
        file.close()


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

    def getSourceList(self):
        return self.configFile.getData('sourcelist', 'name')

    def getLocationList(self):
        return self.configFile.getData('sourcelist', 'location')
