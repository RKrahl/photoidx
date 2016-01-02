"""Geo tools, in particular class GeoPosition.
"""

import sys
import re
import math
from collections import Mapping


# FIXME: for the moment, only support a very basic input format
# "52.518611 N, 13.408333 E".  Should also support alternate formats,
# such as "52 deg 31' 7.0" N, 13 deg 24' 30.0" E".
_geopos_pattern = (r"^\s*(?P<lat>\d+(?:\.\d*))\s*(?P<latref>N|S),\s*"
                   r"(?P<lon>\d+(?:\.\d*))\s*(?P<lonref>E|W)\s*$")
_geopos_re = re.compile(_geopos_pattern)


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

    earthRadius = 6371.0
    """approximate radius of the earth in km."""

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
        elif isinstance(pos, basestring):
            m = _geopos_re.match(pos)
            if m:
                latsign = 1.0 if m.group('latref') == 'N' else -1.0
                self.lat = lat(latsign*float(m.group('lat')))
                lonsign = 1.0 if m.group('lonref') == 'E' else -1.0
                self.lon = lon(lonsign*float(m.group('lon')))
            else:
                raise ValueError("invalid Geo position '%s'." % pos)
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

    def __sub__(self, other):
        """Difference between two GeoPositions.

        Approximate distance of the two points on the earth surface in km, 
        simplifying assumed the earth to be a sphere.
        """
        if isinstance(other, GeoPosition):
            lat1 = math.pi * self.lat / 180.0
            lat2 = math.pi * other.lat / 180.0
            lon1 = math.pi * self.lon / 180.0
            lon2 = math.pi * other.lon / 180.0
            slat = math.sin((lat1-lat2)/2.0)
            slon = math.sin((lon1-lon2)/2.0)
            c1 = math.cos(lat1)
            c2 = math.cos(lat2)
            sigma = 2.0*math.asin(math.sqrt(slat*slat + c1*c2*slon*slon))
            return self.earthRadius * sigma
        else:
            return NotImplemented