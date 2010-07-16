from filesystem import Filesystem

class MockFilesystem (Filesystem):
    def __init__(self):
        Filesystem.__init__(self)
    
    def listDirs(self, root):
        return ['My event', 'event2', 'another event']

"""
    def makeDir(self, dirname):
        if not self.checkValidDir(dirname):
            raise IOError
        if not type(dirname) == list:
            assert False, 'dirname should be list'
"""
