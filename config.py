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
        self.removeItem()
        return ['hello', 'hi']

    def removeItem(self):
        dom = MD.parse(self._configPath)
        items = dom.getElementsByTagName('item')
        sourcelist = dom.getElementsByTagName('sourcelist')[0]
        print dom.toprettyxml()
        sourcelist.removeChild(items[0])
        print dom.toprettyxml()

    def initConfigXml(self):
        root = ET.Element('config')
        sources = [
            {'name':'Memory card', 'location':'D:/'},
            {'name':'Temp folder', 'location':'C:/Photos'}
            ]
        sourcelist = ET.SubElement(root, 'sourcelist')

        for item in sources:
            newItem = ET.SubElement(sourcelist, 'item')
            name = ET.SubElement(newItem, 'name')
            name.text = item['name']
            location = ET.SubElement(newItem, 'location')
            location.text = item['location']

        tree = ET.ElementTree(root)
        tree.write(self.configPath())
        
    
