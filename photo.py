import unittest
import os.path
import Image
from PIL.ExifTags import TAGS

class Photo:
    def __init__(self, root, filename):
        self.imagepath = os.path.join(root, filename)
        self.image = Image.open(self.imagepath)

    def type(self):
        return self.image.format

    def isLandscape(self):
        exif = self.getExif()
        if exif['Orientation'] == 6:
            return False
        width, height = self.image.size
        return width > height

    def getExif(self):
        info = self.image._getexif()
        ret = {}
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
        else:
            ret['Orientation'] = 1
        return ret


class PhotoTests(unittest.TestCase):
    def setUp(self):
        self.root = 'imagesdir'
        self.filename = 'kitten.jpg'
        self.filename2 = 'kitten-portrait.jpg'
        self.filename3 = 'DSC_0015.JPG'
        self.filetype = 'JPEG'
        self.photo = Photo(self.root, self.filename)
        self.photo2 = Photo(self.root, self.filename2)
        self.photo3 = Photo(self.root, self.filename3)

    def testKittenIsJPG(self):
        self.assertEqual(self.filetype, self.photo.type())

    def testKittenIsLandscape(self):
        self.assertTrue(self.photo.isLandscape())

    def testPortraitKittenIsPortrait(self):
        self.assertFalse(self.photo2.isLandscape())

    def testHarmonyIsPortrait(self):
        self.assertFalse(self.photo3.isLandscape())


if __name__ == '__main__':
    unittest.main()
