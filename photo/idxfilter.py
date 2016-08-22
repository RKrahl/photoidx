"""Define filter for photo indices by command line arguments.
"""

import re
import datetime
import argparse
import collections
from photo.geo import GeoPosition

# Need a filter function that returns an iterator.
# With Python 3, the builtin filter() is what we want.  With Python 2,
# filter() returns a list, this is not suitable.  But we can use
# itertools.ifilter in Python 2 instead.
if isinstance(filter(lambda i: True, []), collections.Iterator):
    # Python 3
    ifilter = filter
else:
    # Python 2
    import itertools
    ifilter = itertools.ifilter


class IdxFilter(object):

    def __init__(self, args):
        if args.tags is not None:
            self.taglist = set()
            self.negtaglist = set()
            if args.tags:
                for t in args.tags.split(","):
                    if t.startswith("!"):
                        self.negtaglist.add(t[1:])
                    else:
                        self.taglist.add(t)
        else:
            self.taglist = None
            self.negtaglist = None
        self.select = args.select
        self.date = args.date
        if args.gpspos:
            self.gpspos = args.gpspos
            self.gpsradius = args.gpsradius
        else:
            self.gpspos = None
        self.filelist = set(args.files) if args.files else None

    def __call__(self, item):
        if self.filelist and not item.filename in self.filelist:
            return False
        if self.taglist is not None:
            if not self.taglist <= item.tags:
                return False
            if self.negtaglist & item.tags:
                return False
            if not self.taglist and not self.negtaglist and item.tags:
                return False
        if self.select is not None and item.selected != self.select:
            return False
        if self.date and (item.createDate < self.date[0] or 
                          item.createDate >= self.date[1]):
            return False
        if self.gpspos:
            if (not item.gpsPosition or
                (item.gpsPosition - self.gpspos) > self.gpsradius):
                return False
        return True

    def filter(self, idx):
        return ifilter(self, idx)


_datere = re.compile(r'''^
    (?P<y0>\d{4})-(?P<m0>\d{2})-(?P<d0>\d{2})              # start date
    (?:[T ](?P<h0>\d{2}):(?P<min0>\d{2}):(?P<s0>\d{2}))?   # optional start time
    (?:\s*(?:--|/)\s*                                      # delimeter
      (?P<y1>\d{4})-(?P<m1>\d{2})-(?P<d1>\d{2})            # end date
      (?:[T ](?P<h1>\d{2}):(?P<min1>\d{2}):(?P<s1>\d{2}))? # optional end time
    )?$''', re.X)

def _strpdate(s):
    def _dt(args):
        year, month, day, hour, minute, second = args
        if hour is None:
            return datetime.datetime(int(year), int(month), int(day))
        else:
            return datetime.datetime(int(year), int(month), int(day), 
                                     int(hour), int(minute), int(second))
    match = re.match(_datere, s)
    if match:
        try:
            startdate = _dt(match.group('y0', 'm0', 'd0', 'h0', 'min0', 's0'))
            if match.group('d1') is None:
                if match.group('h0') is None:
                    enddate = startdate + datetime.timedelta(days=1)
                else:
                    enddate = startdate + datetime.timedelta(seconds=1)
            else:
                enddate = _dt(match.group('y1', 'm1', 'd1', 'h1', 'min1', 's1'))
                if match.group('h1') is None:
                    enddate += datetime.timedelta(days=1)
                else:
                    enddate += datetime.timedelta(seconds=1)
            return (startdate, enddate)
        except ValueError:
            pass
    raise argparse.ArgumentTypeError("Invalid date value '%s'" % s)


def addFilterArguments(argparser):
    argparser.add_argument('--tags', 
                           help="select images by comma separated list of tags")
    argparser.add_argument('--selected', 
                           help='select images in the selection', 
                           dest='select', action='store_const', const=True)
    argparser.add_argument('--not-selected', 
                           help='select images not in the selection', 
                           dest='select', action='store_const', const=False)
    argparser.add_argument('--date', type=_strpdate, 
                           help="select images by date")
    argparser.add_argument('--gpspos', 
                           help="select images by GPS position", 
                           type=GeoPosition)
    argparser.add_argument('--gpsradius', type=float, default=3.0, 
                           help="radius around GPS position in km", 
                           metavar='DISTANCE')
    argparser.add_argument('files', nargs='*', 
                           help="select images by file name")
    return argparser
