from filesystem import Filesystem

class Reset:
    def __init__(self):
        self.sourceDir = 'imagesbackup'
        self.destDir = 'imagesdir'
        self.filesystem = Filesystem()
        if not self.filesystem.checkDirExists(self.destDir):
            self.filesystem.makeDir(self.destDir)
        assert self.filesystem.checkDirExists(self.destDir), \
            self.destDir + ' does not exist'

    def fill(self):
        assert self.filesystem.checkDirExists(self.sourceDir), \
            self.sourceDir + ' does not exist'
        self.sourceImages = self.filesystem.listJpegs(self.sourceDir)
        for image in self.sourceImages:
            self.filesystem.copy([self.sourceDir, image],
                                 [self.destDir, image])

    def empty(self, path='', removeDir=True):
        if path == '':
            path = self.destDir
        path = self.filesystem.joinPath(path)
        if not self.filesystem.checkDirExists(path):
            return
        self.destImages = self.filesystem.listJpegs(path)
        for image in self.destImages:
            self.filesystem.removeFile([path, image])
        if removeDir:
            self.filesystem.removeDir(path)
        

if __name__ == '__main__':
    reset = Reset()
    reset.empty()
    reset.empty(['events', 'rugby', 'girls'], removeDir=False)
    reset.empty(['events', 'rugby', 'boys'], removeDir=False)



