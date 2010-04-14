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
