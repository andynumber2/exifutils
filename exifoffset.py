#!/usr/bin/env python


import os, sys
import pyexiv2
import datetime
import time
from optparse import OptionParser


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--days", dest="day_offset", 
                       help="Number of Days (24 hours) to offset EXIF tag", default=0)
    parser.add_option("--hours", dest="hour_offset", 
                       help="Number of Hours to offset EXIF tag", default=0)
    parser.add_option("--minutes", dest="minute_offset",
                       help="Number of Minutes to offset EXIF tag", default=0)
    parser.add_option("--seconds", dest="second_offset",
                       help="Number of Seconds to offset EXIF tag", default=0)
    (options, args) = parser.parse_args()

    day_offset = int(options.day_offset)
    hour_offset = int(options.hour_offset)
    minute_offset = int(options.minute_offset)
    second_offset = int(options.second_offset)

    if len(args) == 0 or not os.path.exists(args[0]):
        sys.stderr.write("Specify file to modify on the command line.\n")
        sys.exit(1)

    file = args[0]

    print "Offset: %s days, %s hours, %s minutes, %s seconds" % 
           (day_offset, hour_offset, minute_offset, second_offset)

    # Now convert everything to seconds.  Mixing signs in the input 
    #   will do weird things.  Prob check for that later
    offset = (day_offset * 24 * 60 * 60) + (hour_offset * 60 * 60) +
             (minute_offset * 60) + second_offset

    delta = datetime.timedelta(days=day_offset, hours=hour_offset, 
                               minutes=minute_offset, seconds=second_offset)

    print "modifying EXIF tag on %s with offset of %s seconds." % (file, offset)

    tag = pyexiv2.Image(file)
    tag.readMetadata()
    for key in ['Exif.Image.DateTime', 'Exif.Photo.DateTimeOriginal', 'Exif.Photo.DateTimeDigitized']:
        print key
        currenttimestamp = tag[key]
        print "    Current Timestamp: %s" % currenttimestamp
        newtimestamp = currenttimestamp + delta
        print "    New Timestamp: %s" % newtimestamp
        tag[key] = newtimestamp
        tag.writeMetadata()
    #print "New Timestamp %s written to %s" % (newtimestamp, file)
    

    



    sys.exit(0)








# vim: tabstop=4 expandtab shiftwidth=4 
