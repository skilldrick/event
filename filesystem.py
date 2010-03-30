import unittest
import os.path
import shutil
    

class Filesystem:
    forbiddenChars = [':', '*', '?', '"', '<', '>', '|']
    
    def join(f):
        def new_f(self, pathname):
            pathname = self.joinPath(pathname)
            return f(self, pathname)
        return new_f

    def join2(f):
        def new_f(self, pathname1, pathname2):
            pathname1 = self.joinPath(pathname1)
            pathname2 = self.joinPath(pathname2)
            return f(self, pathname1, pathname2)
        return new_f
    
    def joinPath(self, dirname):
        if type(dirname) == list:
            dirname = os.path.join(*dirname)
        return dirname

    @join
    def checkDirExists(self, dirname):
        return os.path.exists(dirname)

    @join
    def checkFileExists(self, filename):
        return os.path.exists(filename)

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

    @join
    def removeDir(self, dirname):
        os.rmdir(dirname)

    def listDirs(self, root):
        for x in os.walk(root):
            yield x[0]

    @join
    def listFiles(self, root):
        filenames = os.listdir(root)
        for filename in filenames:
            yield filename

    @join2
    def copy(self, source, destination):
        shutil.copy2(source, destination)

    @join
    def removeFile(self, filename):
        os.remove(filename)
    
        

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
        invalidDir = [self.root, 'some>thing']
        try:
            self.filesystem.makeDir(invalidDir)
            self.fail('makeDir should have raised an IOError')
        except IOError:
            pass

    def testListFiles(self):
        filenames = ['test1', 'test2', 'test3']
        filenamepaths = [os.path.join(self.root, filename)
                         for filename in filenames]
        for filenamepath in filenamepaths:
            f = open(filenamepath, 'w')
            f.close()
        filelist = self.filesystem.listFiles(self.root)
        for file1, file2 in zip(filenames, filelist):
            self.assertEqual(file1, file2)
        for filenamepath in filenamepaths:
            os.remove(filenamepath)

    def testFileExists(self):
        filename = ['imagesdir', 'kitten.jpg']
        self.assertTrue(self.filesystem.checkFileExists(filename))

    def testCopyFile(self):
        source = ['imagesdir', 'kitten.jpg']
        destination = ['testdir', 'testkitten.jpg']
        self.filesystem.copy(source, destination)
        self.assertTrue(self.filesystem.checkFileExists(destination))
        self.filesystem.removeFile(destination)



if __name__ == '__main__':
    unittest.main()

