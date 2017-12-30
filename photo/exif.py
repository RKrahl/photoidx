"""Wrapper around the exif library to extract and convert some information.
"""

import fractions
import warnings
with warnings.catch_warnings():
    # Issue #26
    warnings.simplefilter("ignore")
    from gi.repository import GExiv2


# Some helper classes for exif attributes, having customized string
# representations.

class ExposureTime(fractions.Fraction):
    def __str__(self):
        if self.denominator == 1:
            return "%s sec" % (self.numerator)
        else:
            return "%s/%s sec" % (self.numerator, self.denominator)

class Aperture(float):
    def __str__(self):
        # In fact, we display the reciprocal of the aperture, the
        # f-number, in the string representation.
        if self == int(self):
            return "f/%d" % (int(self))
        else:
            return "f/%.1f" % (float(self))

class FocalLength(float):
    def __str__(self):
        if self == int(self):
            return "%d mm" % (int(self))
        else:
            return "%.1f mm" % (float(self))


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

    @property
    def createDate(self):
        """Time and date the image was taken."""
        try:
            return self._exif.get_date_time()
        except KeyError:
            return None

    @property
    def orientation(self):
        """Orientation of the camera relative to the scene."""
        try:
            orientation = self._exif.get_orientation()
            return self.OrientationXlate[int(orientation)]
        except KeyError:
            return None

    @property
    def gpsPosition(self):
        """GPS coordinates."""
        if ('Exif.GPSInfo.GPSLatitude' in self._exif and
            'Exif.GPSInfo.GPSLongitude' in self._exif):
            lat = self._exif.get_gps_latitude()
            lon = self._exif.get_gps_longitude()
            latref = 'N' if lat >= 0.0 else 'S'
            lonref = 'E' if lon >= 0.0 else 'W'
            return { latref:abs(lat), lonref:abs(lon) }
        else:
            return None

    @property
    def exposureTime(self):
        """Exposure time."""
        try:
            return ExposureTime(self._exif.get_exposure_time())
        except KeyError:
            return None

    @property
    def aperture(self):
        """Aperture."""
        try:
            return Aperture(self._exif.get_fnumber())
        except KeyError:
            return None

    @property
    def focalLength(self):
        """Lens focal length."""
        try:
            return FocalLength(self._exif.get_focal_length())
        except KeyError:
            return None
