import unittest
import os.path
import shutil
    

class Filesystem:
    forbiddenChars = [':', '*', '?', '"', '<', '>', '|']

    def __init__(self):
        pass
    
    def join(f):
        def new_f(self, pathname, extraParam=None):
            pathname = self.joinPath(pathname)
            if extraParam:
                return f(self, pathname, extraParam)
            else:
                return f(self, pathname)
        return new_f

    def join2(f):
        def new_f(self, pathname1, pathname2, extraParam=None):
            pathname1 = self.joinPath(pathname1)
            pathname2 = self.joinPath(pathname2)
            if extraParam:
                return f(self, pathname1, pathname2, extraParam)
            else:
                return f(self, pathname1, pathname2)
        return new_f
    
    def joinPath(self, dirname):
        if type(dirname) == list:
            #just in case any QStrings get through:
            dirname = [str(dir) for dir in dirname]
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

    @join
    def isDir(self, dirname):
        return os.path.isdir(dirname)

    def checkValidDir(self, dirname):
        for char in self.forbiddenChars:
            if char in dirname:
                return False
        return True

    @join
    def removeDir(self, dirname):
        os.rmdir(dirname)

    @join
    def listDirs(self, root):
        ret = []
        for x in os.walk(root):
            ret.append(x)
        ret.sort()
        return ret

    def listToplevelDirs(self, parent):
        try:
            root, dirs, files = os.walk(parent).next()
        except StopIteration: #.next() doesn't work if no dirs
            root, dirs, files = [], [], []
        dirs.sort()
        return dirs

    @join
    def getBasename(self, dirname):
        return os.path.basename(dirname)

    @join
    def listFiles(self, root, extension=None):
        filenames = sorted(os.listdir(root)) #sort filelist for testing
        for filename in filenames:
            if extension:
                if filename.endswith(extension):
                    yield filename
            else:
                yield filename

    def listJpegs(self, root):
        extensions = ('jpg', 'JPG', 'jpeg', 'JPEG')
        return self.listFiles(root, extensions)

    @join2
    def copy(self, source, destination, failOnExist=False):
        if failOnExist and self.checkFileExists(destination):
            raise IOError
        shutil.copy2(source, destination)

    @join
    def removeFile(self, filename):
        os.remove(filename)

    @join
    def getFileSize(self, filename):
        return os.path.getsize(filename)
        

class FilesystemTests(unittest.TestCase):
    newdirs = [
        'testdir',
        ['testdir', 'dir1'],
        ['testdir', 'dir1', 'sub1'],
        ['testdir', 'dir1', 'sub2'],
        ['testdir', 'dir2'],
        ['testdir', 'dir2', 'sub1'],
        ['testdir', 'dir2', 'sub2'],
        ['testdir', 'dir2', 'x, a dir with spaces'],
        ]
    imagesDir = 'imagesdir'
    
    def setUp(self):
        self.root = 'testdir'
        self.longDirname = ['testdir', 'newdir']
        self.filesystem = Filesystem()
        self.filesystem.makeDir(self.root)

    def tearDown(self):
        if self.filesystem.checkDirExists(self.root):
            for filename in self.filesystem.listFiles(self.root):
                if self.filesystem.isDir([self.root, filename]):
                    self.filesystem.removeDir([self.root, filename])
                else:
                    self.filesystem.removeFile([self.root, filename])
            self.filesystem.removeDir(self.root)

    def testGetBasename(self):
        self.assertEqual(self.filesystem.getBasename(self.longDirname),
                         self.longDirname[1])
        
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

    def makeTestDirs(self):
        for newdir in self.newdirs:
            self.filesystem.makeDir(newdir)

    def removeTestDirs(self):
        for newdir in reversed(self.newdirs):
            self.filesystem.removeDir(newdir)

    def testListDirs(self):
        self.makeTestDirs()
        dirlist = self.filesystem.listDirs(self.root)
        for listitem, diritem in zip(dirlist, self.newdirs):
            self.assertEqual(listitem[0], self.filesystem.joinPath(diritem))
        self.removeTestDirs()
        
    def testListTopLevelDirs(self):
        self.makeTestDirs()
        testToplevelDirs = ['dir1', 'dir2']
        toplevelDirs = self.filesystem.listToplevelDirs(self.root)
        for toplevelDir, testToplevelDir in zip(toplevelDirs,
                                                testToplevelDirs):
            self.assertEqual(toplevelDir, testToplevelDir)
        self.removeTestDirs()

    def testTopLevelDirsOnNonExistentDir(self):
        self.filesystem.listToplevelDirs('nonexistentdir')

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
        self.makeFiles(filenames)
        filelist = self.filesystem.listFiles(self.root)
        for file1, file2 in zip(filenames, filelist):
            self.assertEqual(file1, file2)
        self.removeFiles(filenames)

    def makeFiles(self, filenames):
        filenamepaths = [os.path.join(self.root, filename)
                         for filename in filenames]
        for filenamepath in filenamepaths:
            f = open(filenamepath, 'w')
            f.close()

    def removeFiles(self, filenames):
        filenamepaths = [os.path.join(self.root, filename)
                         for filename in filenames]
        for filenamepath in filenamepaths:
            os.remove(filenamepath)

    def testListJpegs(self):
        filenames = ['test1.jpg', 'test2.jpeg', 'test3.JPG', 'test.png']
        validFilenames = filenames[:3]
        self.makeFiles(filenames)
        filelist = self.filesystem.listJpegs(self.root)
        for file1, file2 in zip(validFilenames, filelist):
            self.assertEqual(file1, file2)
        self.removeFiles(filenames)

    def testFileExists(self):
        filename = [self.imagesDir, 'kitten.jpg']
        self.assertTrue(self.filesystem.checkFileExists(filename))

    def testCopyFile(self):
        source = [self.imagesDir, 'kitten.jpg']
        destination = ['testdir', 'testkitten.jpg']
        self.filesystem.copy(source, destination)
        self.assertTrue(self.filesystem.checkFileExists(destination))
        self.filesystem.removeFile(destination)

    def testCopyOverFile(self):
        file1 = [self.imagesDir, 'The Garden 17th June 017.JPG']
        file2 = [self.imagesDir, 'The Garden 17th June 019.JPG']
        file1Size = self.filesystem.getFileSize(file1)
        file2Size = self.filesystem.getFileSize(file2)
        self.assertNotEqual(file1Size, file2Size,
                            'Files under test are equal size already')
        self.filesystem.copy(file1, file2)
        file2NewSize = self.filesystem.getFileSize(file2)
        self.assertEqual(file1Size, file2NewSize,
                         'Didn\'t copy over file')

    def testCopyOverFileWithFail(self):
        file1 = [self.imagesDir, 'The Garden 17th June 015.JPG']
        file2 = [self.imagesDir, 'The Garden 17th June 016.JPG']
        file1Size = self.filesystem.getFileSize(file1)
        file2Size = self.filesystem.getFileSize(file2)
        try:
            self.filesystem.copy(file1, file2, True)
            self.fail('Copy did not raise exception')
        except IOError:
            pass


def suite():
    testSuite = unittest.makeSuite(FilesystemTests)
    return testSuite
        

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())

