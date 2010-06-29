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

    def empty(self):
        self.destImages = self.filesystem.listJpegs(self.destDir)
        for image in self.destImages:
            self.filesystem.removeFile([self.destDir, image])
        self.filesystem.removeDir(self.destDir)
        

if __name__ == '__main__':
    reset = Reset()
    reset.empty()



