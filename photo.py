import unittest
import os.path
import Image

class Photo:
    def __init__(self, root, filename):
        self.imagepath = os.path.join(root, filename)
        self.image = Image.open(self.imagepath)

    def type(self):
        return self.image.format

    def isLandscape(self):
        width, height = self.image.size
        return width > height


class PhotoTests(unittest.TestCase):
    def setUp(self):
        self.root = 'imagesdir'
        self.filename = 'kitten.jpg'
        self.filename2 = 'kitten-portrait.jpg'
        self.filetype = 'JPEG'
        self.photo = Photo(self.root, self.filename)
        self.photo2 = Photo(self.root, self.filename2)

    def testKittenIsJPG(self):
        self.assertEqual(self.filetype, self.photo.type())

    def testKittenIsLandscape(self):
        self.assertTrue(self.photo.isLandscape())

    def testPortraitKittenIsPortrait(self):
        self.assertFalse(self.photo2.isLandscape())


if __name__ == '__main__':
    unittest.main()
