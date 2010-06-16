import optparse
import sys

from gui import gui


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("-t", "--test", action="store_true")
    options, args = parser.parse_args()
    #This needs to be done to make sure unittest doesn't break
    del sys.argv[1:]
    if options.test:
        gui.test()
    else:
        gui.main()

