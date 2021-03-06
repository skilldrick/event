import unittest
import os.path
import gc
import Image
from PIL.ExifTags import TAGS

from featurebroker import *

class Orientation:
    LANDSCAPE = 0
    PORTRAIT = 1
    CW_LANDSCAPE = 2
    CW_PORTRAIT = 3
    CCW_LANDSCAPE = 4
    CCW_PORTRAIT = 5
    FLIPPED_LANDSCAPE = 6
    FLIPPED_PORTRAIT = 7
    

class Photo:
    filesystem = RequiredFeature('Filesystem')
    
    def __init__(self, root, filename=None):
        if filename == None:
            self.path = root
        else:
            self.path = self.filesystem.joinPath([root, filename])

        self.openPhoto()
        self.orientation = self.calculateOrientation()

    def openPhoto(self, slow=False):
        if slow:
            #This is the way to do it to ensure the image is closed.
            #Deleting image achieves the same effect so not needed.
            imageFile = open(self.path, 'rb')
            self.image = Image.open(imageFile)
            self.image.load()
            imageFile.close()
        else:
            self.image = Image.open(self.path)

    def type(self):
        return self.image.format

    def getPath(self):
        return self.path

    def isLandscape(self):
        width, height = self.image.size
        return width > height

    def calculateOrientation(self):
        """Set up a table with all orientation options.
        Table is indexed by rotation and shape."""
        orientation = [
            [Orientation.LANDSCAPE,         Orientation.PORTRAIT],
            [Orientation.CW_LANDSCAPE,      Orientation.CW_PORTRAIT],
            [Orientation.CCW_LANDSCAPE,     Orientation.CCW_PORTRAIT],
            [Orientation.FLIPPED_LANDSCAPE, Orientation.FLIPPED_PORTRAIT],
            ]
        exif = self.getExif()
        if exif and exif['Orientation'] == 3: #180
            rotation = 3
        elif exif and exif['Orientation'] == 6: #90 CCW
            rotation = 2
        elif exif and exif['Orientation'] == 8: #90 CW
            rotation = 1
        else:
            rotation = 0

        if self.isLandscape():
            return orientation[rotation][0]
        else:
            return orientation[rotation][1]

    def rotatedCW(self):
        return self.orientation == Orientation.CW_LANDSCAPE or \
            self.orientation == Orientation.CW_PORTRAIT

    def rotatedCCW(self):
        return self.orientation == Orientation.CCW_LANDSCAPE or \
            self.orientation == Orientation.CCW_PORTRAIT

    def rotated180(self):
        return self.orientation == Orientation.FLIPPED_LANDSCAPE or \
            self.orientation == Orientation.FLIPPED_PORTRAIT

    def getExif(self):
        info = self.image._getexif()
        ret = {}
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
        else:
            ret = None
        return ret

    def rotateImage(self):
        if self.rotatedCCW():
            self.image = self.image.rotate(-90)
        elif self.rotatedCW():
            self.image = self.image.rotate(90)
        elif self.rotated180():
            self.image = self.image.rotate(180)

    def save(self, path):
        self.rotateImage()
        path = self.filesystem.joinPath(path)
        self.image.save(path)

    def close(self):
        #This is needed so Windows won't think the file is still in use.
        del self.image
        gc.collect() #Belt and braces (not necessarily necessary).


class PhotoTests(unittest.TestCase):
    def setUp(self):
        self.root = 'imagesdir'
        self.filenames = []
        self.filenames.append('kitten.jpg')
        self.filenames.append('kitten-portrait.jpg')
        self.filenames.append('DSC_0015.JPG')
        self.filenames.append('DSC_0004.JPG')
        self.filetype = 'JPEG'
        self.photos = []
        for filename in self.filenames:
            self.photos.append(Photo(self.root, filename))

    def testPhotosAreJpeg(self):
        for photo in self.photos:
            self.assertEqual(self.filetype, photo.type())

    def testOrientation(self):
        self.assertEqual(self.photos[0].orientation, 0)
        self.assertEqual(self.photos[1].orientation, 1)
        self.assertEqual(self.photos[2].orientation, 4)
        self.assertEqual(self.photos[3].orientation, 0)

def suite():
    testSuite = unittest.makeSuite(PhotoTests)
    return testSuite


if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
