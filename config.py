import xml.etree.ElementTree as ET
import xml.dom.minidom as MD

class Config:
    _eventsDir = 'events'
    _configPath = 'config.xml'
    
    def __init__(self):
        pass

    def eventsDir(self):
        return self._eventsDir

    def configPath(self):
        return self._configPath

    def setEvent(self, event):
        self._event = event

    def getEvent(self):
        return self._event

    def getSourceList(self):
        #self.initConfigXml()
        return ['hello', 'hi']

    def removeItem(self):
        dom = MD.parse(self._configPath)
        items = dom.getElementsByTagName('item')
        sourcelist = dom.getElementsByTagName('sourcelist')[0]
        print dom.toprettyxml()
        sourcelist.removeChild(items[0])
        print dom.toprettyxml()

    def addSubElement(self, dom, parent, name, contents=None):
        newElement = dom.createElement(name)
        parent.appendChild(newElement)
        if not contents == None:
            text = dom.createTextNode(contents)
            newElement.appendChild(text)
        return newElement

    def initConfigXml(self):
        dom = MD.parseString('<config />')
        root = dom.childNodes[0]
        sourcelist = self.addSubElement(dom, root, 'sourcelist')

        sources = [
            {'name':'Memory card', 'location':'D:/'},
            {'name':'Temp folder', 'location':'C:/Photos'}
            ]

        for item in sources:
            newItem = self.addSubElement(dom, sourcelist, 'item')
            self.addSubElement(dom, newItem, 'name', item['name'])
            self.addSubElement(dom, newItem, 'location', item['location'])

        file = open(self.configPath(), 'w')
        root.writexml(file)
        file.close()
    
