import unittest

from featurebroker import *
from config import Config
from filesystem import Filesystem


class Category:
    children = []

    def __init__(self, name):
        self.name = name


class CategoryTree:
    def __init__(self):
        self.root = None

    def addNode(self, name):
        return Category(name)

    def insert(self, root, name):
        self.children.append(self.addNode(name))
        
"""Are the children in Category or in CategoryTree?
c.f. http://code.activestate.com/recipes/286239/"""

class Categories:
    filesystem = RequiredFeature('Filesystem')

    def __init__(self):
        self.recurseList(self.filesystem.listDirs(['events', 'rugby']))

    def searchList(self, needle, categoryList):
        for index, category in enumerate(categoryList):
            if category[0] == needle:
                return index
        return -1

    def recurseList(self, categoryList):
        firstItem = categoryList[0]
        children = firstItem[1]
        if len(children) == 0:
            return
        else:
            for child in children:
                
                path = self.filesystem.joinPath([firstItem[0], child])
                print self.categoryName(path), '  ', path
                index = self.searchList(path, categoryList)
                self.recurseList(categoryList[index:])
                

    def categoryName(self, dirname):
        return self.filesystem.getBasename(dirname)


class CategoriesTests(unittest.TestCase):
    def setUp(self):
        self.categories = Categories()

    def testTest(self):
        pass


class MockFilesystem(Filesystem):
    def listDirs(self, dirname):
        return [
            ('events/rugby', ['boys', 'girls'], []),
            ('events/rugby/boys', ['under 7s', 'under 8s', 'under 9s'], []),
            ('events/rugby/boys/under 7s', ['match 1', 'match 2'], []),
            ('events/rugby/boys/under 7s/match 1', [], []),
            ('events/rugby/boys/under 7s/match 2', [], []),
            ('events/rugby/boys/under 8s', [], []),
            ('events/rugby/boys/under 9s', [], []),
            ('events/rugby/girls', ['under 10s', 'over 10s'], []),
            ('events/rugby/girls/under 10s', [], []),
            ('events/rugby/girls/over 10s', [], []),
            ]



def suite():
    features.provide('Filesystem', MockFilesystem)
    features.provide('Config', Config)
    testSuite = unittest.makeSuite(CategoriesTests)
    return testSuite

    
def main():
    unittest.TextTestRunner().run(suite())

if __name__ == '__main__':
    main()


