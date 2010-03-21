import unittest
import os.path
import Image

class Photo:
    def __init__(self, root, filename):
        self.imagepath = os.path.join(root, filename)
        self.image = Image.open(self.imagepath)

    def type(self):
        return self.image.format


class PhotoTests(unittest.TestCase):
    def setUp(self):
        self.root = 'imagesdir'
        self.filename = 'kitten.jpg'
        self.filetype = 'JPEG'
        self.photo = Photo(self.root, self.filename)

    def testKittenIsJPG(self):
        self.assertEqual(self.filetype, self.photo.type())


if __name__ == '__main__':
    unittest.main()
