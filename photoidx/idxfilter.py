"""Define filter for photo indices by command line arguments.
"""

import argparse
import datetime
from pathlib import Path
import re
from photoidx.geo import GeoPosition


_datere = re.compile(r'''^
    (?P<y0>\d{4})-(?P<m0>\d{2})-(?P<d0>\d{2})              # start date
    (?:[T ](?P<h0>\d{2}):(?P<min0>\d{2}):(?P<s0>\d{2}))?   # optional start time
    (?:\s*(?:--|/)\s*                                      # delimeter
      (?P<y1>\d{4})-(?P<m1>\d{2})-(?P<d1>\d{2})            # end date
      (?:[T ](?P<h1>\d{2}):(?P<min1>\d{2}):(?P<s1>\d{2}))? # optional end time
    )?$''', re.X)

def strpdate(s):
    """Parse a date and time intervall.
    """
    def _dt(args):
        year, month, day, hour, minute, second = args
        if hour is None:
            return datetime.datetime(int(year), int(month), int(day))
        else:
            return datetime.datetime(int(year), int(month), int(day), 
                                     int(hour), int(minute), int(second))
    match = re.match(_datere, s)
    if not match:
        raise ValueError("Invalid date value '%s'" % s)
    startdate = _dt(match.group('y0', 'm0', 'd0', 'h0', 'min0', 's0'))
    if match.group('d1') is None:
        if match.group('h0') is None:
            enddate = startdate + datetime.timedelta(days=1)
        else:
            enddate = startdate + datetime.timedelta(seconds=1)
    else:
        enddate = _dt(match.group('y1', 'm1', 'd1', 'h1', 'min1', 's1'))
    return (startdate, enddate)


class IdxFilter(object):

    @classmethod
    def from_args(cls, args):
        kwargs = {}
        for a in ("tags", "select", "date", "gpspos", "gpsradius", "files"):
            kwargs[a] = getattr(args, a)
        return cls(**kwargs)

    def __init__(self, 
                 tags=None, select=None, date=None, 
                 gpspos=None, gpsradius=3.0, files=None):
        if tags is not None:
            self.taglist = set()
            self.negtaglist = set()
            if tags:
                for t in tags.split(","):
                    if t.startswith("!"):
                        self.negtaglist.add(t[1:])
                    else:
                        self.taglist.add(t)
        else:
            self.taglist = None
            self.negtaglist = None
        self.select = select
        self.date = date
        if gpspos:
            self.gpspos = gpspos
            self.gpsradius = gpsradius
        else:
            self.gpspos = None
            self.gpsradius = None
        if files:
            self.filelist = { Path(f) for f in files }
        else:
            self.filelist = None

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
        return filter(self, idx)


def addFilterArguments(argparser):
    def _strpdate_arg(s):
        try:
            return strpdate(s)
        except ValueError:
            raise argparse.ArgumentTypeError("Invalid date value '%s'" % s)

    argparser.add_argument('--tags', 
                           help="select images by comma separated list of tags")
    argparser.add_argument('--selected', 
                           help='select images in the selection', 
                           dest='select', action='store_const', const=True)
    argparser.add_argument('--not-selected', 
                           help='select images not in the selection', 
                           dest='select', action='store_const', const=False)
    argparser.add_argument('--date', type=_strpdate_arg, 
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
