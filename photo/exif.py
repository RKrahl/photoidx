"""Wrapper around the exif library to extract and convert some information.
"""

import pyexiv2


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
        self._exif = pyexiv2.ImageMetadata(filename)
        self._exif.read()
        self.createdate = self._exif['Exif.Photo.DateTimeDigitized'].value
        orientation = self._exif['Exif.Image.Orientation'].value
        self.orientation = self.OrientationXlate[orientation]
        if ('Exif.GPSInfo.GPSLatitude' in self._exif.exif_keys and
            'Exif.GPSInfo.GPSLongitude' in self._exif.exif_keys):
            lat = self._exif['Exif.GPSInfo.GPSLatitude'].value
            latref = self._exif['Exif.GPSInfo.GPSLatitudeRef'].value
            lon = self._exif['Exif.GPSInfo.GPSLongitude'].value
            lonref = self._exif['Exif.GPSInfo.GPSLongitudeRef'].value
            self.gpsPosition = {latref:float(lat[0] + lat[1]/60 + lat[2]/3600),
                                lonref:float(lon[0] + lon[1]/60 + lon[2]/3600)}
        else:
            self.gpsPosition = None

