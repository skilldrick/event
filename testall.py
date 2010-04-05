import unittest

import eventlist
import filesystem
import photo


def main():
    suites = []
    suites.append(eventlist.suite())
    suites.append(filesystem.suite())
    suites.append(photo.suite())
    allTests = unittest.TestSuite(suites)
    runner = unittest.TextTestRunner()
    runner.run(allTests)


if __name__ == '__main__':
    main()
