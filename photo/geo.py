"""Geo tools, in particular class GeoPosition.
"""

import sys
from collections import Mapping


class deg(float):
    """A degree as float that can be converted to (degree, minute, second).
    """
    def __abs__(self):
        return deg(super(deg, self).__abs__())
    def dms(self):
        dg = int(self)
        dm = int(60*(self-dg))
        ds = 60*(60*(self-dg)-dm)
        return (dg, dm, ds)

class lat(deg):
    """Latitude, which is either N or S.
    """
    def ref(self):
        return 'N' if self >= 0 else 'S'
    def dmsref(self):
        return abs(self).dms() + (self.ref(),)

class lon(deg):
    """Longitude, which is either E or W.
    """
    def ref(self):
        return 'E' if self >= 0 else 'W'
    def dmsref(self):
        return abs(self).dms() + (self.ref(),)


class GeoPosition(object):

    def __init__(self, pos):
        if isinstance(pos, Mapping):
            if 'N' in pos and 'S' not in pos:
                self.lat = lat(pos['N'])
            elif 'S' in pos and 'N' not in pos:
                self.lat = lat(-pos['S'])
            else:
                raise ValueError("invalid Geo position %s: "
                                 "must have either 'N' or 'S' in keys." 
                                 % str(pos))
            if 'E' in pos and 'W' not in pos:
                self.lon = lon(pos['E'])
            elif 'W' in pos and 'E' not in pos:
                self.lon = lon(-pos['W'])
            else:
                raise ValueError("invalid Geo position %s: "
                                 "must have either 'E' or 'W' in keys." 
                                 % str(pos))
            # FIXME: add conversion from str
        else:
            raise TypeError("invalid type '%s'" % type(pos))

    if sys.version_info < (3, 0):

        def __str__(self):
            return ("%d deg %d' %.2f\" %s, %d deg %d' %.2f\" %s"
                    % (self.lat.dmsref() + self.lon.dmsref()))

        def __unicode__(self):
            return (u"%d\xb0 %d\u2032 %.2f\u2033 %s, "
                    u"%d\xb0 %d\u2032 %.2f\u2033 %s"
                    % (self.lat.dmsref() + self.lon.dmsref()))

    else:

        def __str__(self):
            return (u"%d\xb0 %d\u2032 %.2f\u2033 %s, "
                    u"%d\xb0 %d\u2032 %.2f\u2033 %s"
                    % (self.lat.dmsref() + self.lon.dmsref()))

    def as_dict(self):
        return {
            self.lat.ref(): float(abs(self.lat)),
            self.lon.ref(): float(abs(self.lon))
        }
