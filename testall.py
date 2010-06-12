import unittest

import eventlist
import filesystem
import photo
import importer
import config


def main():
    suites = []
    suites.append(eventlist.suite())
    suites.append(filesystem.suite())
    suites.append(photo.suite())
    suites.append(importer.suite())
    suites.append(config.suite())
    allTests = unittest.TestSuite(suites)
    runner = unittest.TextTestRunner()
    runner.run(allTests)


if __name__ == '__main__':
    main()
