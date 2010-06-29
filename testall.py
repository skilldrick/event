import unittest

import eventlist
import filesystem
import photo
import importer
import config
from reset import Reset


def main():
    suites = []
    suites.append(eventlist.suite())
    suites.append(filesystem.suite())
    suites.append(photo.suite())
    suites.append(importer.suite())
    suites.append(config.suite())
    allTests = unittest.TestSuite(suites)
    runner = unittest.TextTestRunner()
    reset = Reset()
    reset.fill() #fill imagesdir with images
    runner.run(allTests)
    reset.empty() #delete images in imagesdir


if __name__ == '__main__':
    main()
