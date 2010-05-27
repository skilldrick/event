import unittest

import eventlist
import filesystem
import photo
import categories
import importer


def main():
    suites = []
    suites.append(eventlist.suite())
    suites.append(filesystem.suite())
    suites.append(photo.suite())
    suites.append(categories.suite())
    suites.append(importer.suite())
    allTests = unittest.TestSuite(suites)
    runner = unittest.TextTestRunner()
    runner.run(allTests)


if __name__ == '__main__':
    main()
