"""Wrapper around the exif library to extract and convert some information.
"""

from gi.repository import GExiv2


class Exif(object):

    OrientationXlate = {
        1: 'Horizontal (normal)',
        2: 'Mirror horizontal',
        3: 'Rotate 180',
        4: 'Mirror vertical',
        5: 'Mirror horizontal and rotate 270 CW',
        6: 'Rotate 90 CW',
        7: 'Mirror horizontal and rotate 90 CW',
        8: 'Rotate 270 CW',
    }

    def __init__(self, filename):
        self._exif = GExiv2.Metadata(filename)
        self.createdate = self._exif.get_date_time()
        orientation = self._exif.get_orientation()
        self.orientation = self.OrientationXlate[int(orientation)]
        if ('Exif.GPSInfo.GPSLatitude' in self._exif and
            'Exif.GPSInfo.GPSLongitude' in self._exif):
            lat = self._exif.get_gps_latitude()
            lon = self._exif.get_gps_longitude()
            latref = 'N' if lat >= 0.0 else 'S'
            lonref = 'E' if lon >= 0.0 else 'W'
            self.gpsPosition = { latref:abs(lat), lonref:abs(lon) }
        else:
            self.gpsPosition = None

