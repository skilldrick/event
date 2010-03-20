import unittest
import os.path

    

class Filesystem:
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
        if not self.checkDirExists(dirname):
            os.makedirs(dirname)

    def joinPath(self, dirname):
        if type(dirname) == list:
            dirname = os.path.join(*dirname)
        return dirname

    @join
    def removeDir(self, dirname):
        os.rmdir(dirname)
        


class FilesystemTests(unittest.TestCase):
    def setUp(self):
        self.longDirname = ['testdir', 'newdir']
        self.filesystem = Filesystem()
        
    def testCheckDirExists(self):
        self.assertTrue(self.filesystem.checkDirExists('testdir'))

    def testCheckDirDoesntExist(self):
        self.assertFalse(self.filesystem.checkDirExists('fakedir'))

    def testMakeDir(self):
        self.filesystem.makeDir(self.longDirname)
        success = self.filesystem.checkDirExists(self.longDirname)
        self.assertTrue(success)

    def testMakeExistingDir(self):
        dirname = 'testdir'
        self.filesystem.makeDir(dirname)
        success = self.filesystem.checkDirExists(dirname)
        self.assertTrue(success)

    def testRemoveDir(self):
        self.filesystem.makeDir(self.longDirname)
        self.filesystem.removeDir(self.longDirname)
        self.assertFalse(self.filesystem.checkDirExists(self.longDirname))


if __name__ == '__main__':
    unittest.main()

                       
        
