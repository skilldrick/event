import unittest
import os.path
    

class Filesystem:
    forbiddenChars = [':', '*', '?', '"', '<', '>', '|']
    
    def join(f):
        def new_f(self, dirname):
            dirname = self.joinPath(dirname)
            return f(self, dirname)
        return new_f
    
    @join
    def checkDirExists(self, dirname):
        return os.path.exists(dirname)

    @join
    def makeDir(self, dirname):
        if not self.checkValidDir(dirname):
            raise IOError
        if not self.checkDirExists(dirname):
            os.makedirs(dirname)

    def checkValidDir(self, dirname):
        for char in self.forbiddenChars:
            if char in dirname:
                return False
        return True

    def joinPath(self, dirname):
        if type(dirname) == list:
            dirname = os.path.join(*dirname)
        return dirname

    @join
    def removeDir(self, dirname):
        os.rmdir(dirname)

    def listDirs(self, root):
        for x in os.walk(root):
            yield x[0]

    


class FilesystemTests(unittest.TestCase):
    def setUp(self):
        self.root = 'testdir'
        self.longDirname = ['testdir', 'newdir']
        self.filesystem = Filesystem()
        self.filesystem.makeDir(self.root)
        
    def testCheckDirExists(self):
        self.assertTrue(self.filesystem.checkDirExists(self.root))

    def testCheckDirDoesntExist(self):
        self.assertFalse(self.filesystem.checkDirExists('fakedir'))

    def testMakeDir(self):
        self.filesystem.makeDir(self.longDirname)
        success = self.filesystem.checkDirExists(self.longDirname)
        self.assertTrue(success)

    def testMakeExistingDir(self):
        self.filesystem.makeDir(self.root)
        success = self.filesystem.checkDirExists(self.root)
        self.assertTrue(success)

    def testRemoveDir(self):
        self.filesystem.makeDir(self.longDirname)
        self.filesystem.removeDir(self.longDirname)
        self.assertFalse(self.filesystem.checkDirExists(self.longDirname))

    def testListDirs(self):
        newdirs = [
            'testdir',
            ['testdir', 'dir1'],
            ['testdir', 'dir1', 'sub1'],
            ['testdir', 'dir1', 'sub2'],
            ['testdir', 'dir2'],
            ['testdir', 'dir2', 'sub1'],
            ['testdir', 'dir2', 'sub2'],
            ]
        for newdir in newdirs:
            self.filesystem.makeDir(newdir)
        dirlist = self.filesystem.listDirs(self.root)
        for listitem, diritem in zip(dirlist, newdirs):
            self.assertEqual(listitem, self.filesystem.joinPath(diritem))
        for newdir in reversed(newdirs):
            self.filesystem.removeDir(newdir)

    def testValidDirs(self):
        validNames = [
            'hello',
            'dir1',
            'monkey%',
            ]
        for name in validNames:
            self.assertTrue(self.filesystem.checkValidDir(name))
            
    def testInvalidDir(self):
        invalidNames = [
            'dave<dave',
            'fish"1',
            'this*',
            'pipe|pipe',
            ]
        for name in invalidNames:
            self.assertFalse(self.filesystem.checkValidDir(name))

    def testCreateInvalidDir(self):
        invalidDir = ['testdir', 'some>thing']
        try:
            self.filesystem.makeDir(invalidDir)
            self.fail('makeDir should have raised an IOError')
        except IOError:
            pass


if __name__ == '__main__':
    unittest.main()

