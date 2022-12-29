"""Wrapper around the exif library to extract and convert some information.
"""

import datetime
import fractions
import warnings
import exifread

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

    def __init__(self, path):
        with path.open("rb") as f:
            self._tags = exifread.process_file(f)

    @property
    def createDate(self):
        """Time and date the image was taken."""
        try:
            dt = self._tags['Image DateTime'].values
        except (AttributeError, KeyError):
            return None
        else:
            return datetime.datetime.strptime(dt, "%Y:%m:%d %H:%M:%S")

    @property
    def orientation(self):
        """Orientation of the camera relative to the scene."""
        try:
            orientation = self._tags['Image Orientation'].values[0]
        except (AttributeError, KeyError):
            return None
        else:
            return self.OrientationXlate[int(orientation)]

    @property
    def gpsPosition(self):
        """GPS coordinates."""
        try:
            lat_tuple = self._tags['GPS GPSLatitude'].values
            lon_tuple = self._tags['GPS GPSLongitude'].values
            latref = self._tags['GPS GPSLatitudeRef'].values
            lonref = self._tags['GPS GPSLongitudeRef'].values
        except (AttributeError, KeyError):
            return None
        else:
            lat = lat_tuple[0] + lat_tuple[1]/60 + lat_tuple[2]/3600
            lon = lon_tuple[0] + lon_tuple[1]/60 + lon_tuple[2]/3600
            return { latref:float(lat), lonref:float(lon) }

    @property
    def cameraModel(self):
        """Camera Model."""
        try:
            return self._tags['Image Model'].values
        except (AttributeError, KeyError):
            return None

    @property
    def exposureTime(self):
        """Exposure time."""
        try:
            et = self._tags['EXIF ExposureTime'].values[0]
        except (AttributeError, KeyError):
            return None
        else:
            return ExposureTime(et)

    @property
    def aperture(self):
        """Aperture."""
        try:
            f = self._tags['EXIF FNumber'].values[0]
        except (AttributeError, KeyError):
            return None
        else:
            return Aperture(f)

    @property
    def iso(self):
        """ISO speed rating."""
        try:
            return self._tags['EXIF ISOSpeedRatings'].values[0]
        except (AttributeError, KeyError):
            return None

    @property
    def focalLength(self):
        """Lens focal length."""
        try:
            fl = self._tags['EXIF FocalLength'].values[0]
        except (AttributeError, KeyError):
            return None
        else:
            return FocalLength(fl)
