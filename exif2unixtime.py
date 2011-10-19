#!/usr/bin/env python


import os, sys
import pyexiv2
import datetime
import shutil
from time import mktime


from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option("-i", dest="input", help="Input Directory", default=None)
    parser.add_option("-o", dest="output", help="Output Directory", default=None)
    (options, args) = parser.parse_args()

    if options.input is None or options.output is None:
        sys.stderr.write("Specify Input and Output directories (-i -o)\n")
        sys.exit(1)
    input = options.input
    output = options.output

    sys.stderr.write("Input directory: %s, Output directory: %s\n" % (input, output))

    if not os.path.isdir(input) or not os.path.isdir(output):
        sys.stderr.write("Input or Output directory doesn't exist!\n")
        sys.exit(1)

    for root, dirs, files in os.walk(input):
        for file in files:
            inputpath = os.path.join(root, file)
            try:
                tag = pyexiv2.Image(inputpath)
                tag.readMetadata()
                timestamp = tag['Exif.Photo.DateTimeOriginal']
                extension = file.split('.')[-1]

                # UNIX timestamp way
                for i in range(1, 101):
                    outputpath = os.path.join(output, "%s%02d.%s" % (str( int( mktime( timestamp.timetuple()))), i, extension))
                    outputpath = os.path.join(output, "%s%02d.%s" % (timestamp.strftime("%y%m%d%H%M%S"), i, extension))
                    if not os.path.exists(outputpath):
                        print "mv %s %s" % (inputpath, outputpath)
                        shutil.move(inputpath, outputpath)
                        break
                if i == 100:
                    sys.stderr.write("WARNING: can't process %s, more than 100 files with same timestamp\n" % inputpath)
            except IOError:
                sys.stderr.write("Can't open %s or read EXIF tag.  Skipping.\n" % inputpath)





# vim: tabstop=4 expandtab shiftwidth=4
