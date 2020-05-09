"""Wrapper around the exif library to extract and convert some information.
"""

import datetime
import fractions
import warnings
import exif

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
            self._exif = exif.Image(f)

    @property
    def createDate(self):
        """Time and date the image was taken."""
        try:
            dt = self._exif.datetime_original
        except (AttributeError, KeyError):
            return None
        else:
            return datetime.datetime.strptime(dt, "%Y:%m:%d %H:%M:%S")

    @property
    def orientation(self):
        """Orientation of the camera relative to the scene."""
        try:
            orientation = self._exif.orientation
        except (AttributeError, KeyError):
            return None
        else:
            return self.OrientationXlate[int(orientation)]

    @property
    def gpsPosition(self):
        """GPS coordinates."""
        try:
            lat_tuple = self._exif.gps_latitude
            lon_tuple = self._exif.gps_longitude
            latref = self._exif.gps_latitude_ref
            lonref = self._exif.gps_longitude_ref
        except (AttributeError, KeyError):
            return None
        else:
            lat = lat_tuple[0] + lat_tuple[1]/60 + lat_tuple[2]/3600
            lon = lon_tuple[0] + lon_tuple[1]/60 + lon_tuple[2]/3600
            return { latref:lat, lonref:lon }

    @property
    def cameraModel(self):
        """Camera Model."""
        try:
            return self._exif.model
        except (AttributeError, KeyError):
            return None

    @property
    def exposureTime(self):
        """Exposure time."""
        try:
            et = self._exif.exposure_time
        except (AttributeError, KeyError):
            return None
        else:
            return ExposureTime(fractions.Fraction(et).limit_denominator())

    @property
    def aperture(self):
        """Aperture."""
        try:
            f = self._exif.f_number
        except (AttributeError, KeyError):
            return None
        else:
            return Aperture(f)

    @property
    def iso(self):
        """ISO speed rating."""
        try:
            return self._exif.photographic_sensitivity
        except (AttributeError, KeyError):
            return None

    @property
    def focalLength(self):
        """Lens focal length."""
        try:
            fl = self._exif.focal_length
        except (AttributeError, KeyError):
            return None
        else:
            return FocalLength(fl)
