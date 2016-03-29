"""Provide the class IdxItem which represents an item in the index.
"""

import hashlib
from photo.exif import Exif
from photo.geo import GeoPosition


def _checksum(fname):
    """Calculate the md5 hash for a file.
    """
    m = hashlib.md5()
    chunksize = 8192
    with open(fname, 'rb') as f:
        while True:
            chunk = f.read(chunksize)
            if not chunk:
                break
            m.update(chunk)
    return {'md5': m.hexdigest()}


class IdxItem(object):

    def __init__(self, filename=None, data=None):
        self.filename = None
        self.tags = []
        if data is not None:
            if 'md5' in data:
                data['checksum'] = {'md5': data['md5']}
                del data['md5']
            self.__dict__.update(data)
        elif filename is not None:
            self.filename = filename
            self.checksum = _checksum(filename)
            exifdata = Exif(filename)
            self.createdate = exifdata.createdate
            self.orientation = exifdata.orientation
            self.gpsPosition = exifdata.gpsPosition
        if self.gpsPosition:
            self.gpsPosition = GeoPosition(self.gpsPosition)
        self.tags = set(self.tags)

    def as_dict(self):
        d = self.__dict__.copy()
        d['tags'] = list(d['tags'])
        d['tags'].sort()
        if d['gpsPosition']:
            d['gpsPosition'] = d['gpsPosition'].as_dict()
        return d
