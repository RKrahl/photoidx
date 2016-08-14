"""Provide the class IdxItem which represents an item in the index.
"""

import os.path
import hashlib
from photo.exif import Exif
from photo.geo import GeoPosition


def _checksum(fname, hashalg):
    """Calculate the md5 hash for a file.
    """
    if not hashalg:
        return {}
    m = { h:hashlib.new(h) for h in hashalg }
    chunksize = 8192
    with open(fname, 'rb') as f:
        while True:
            chunk = f.read(chunksize)
            if not chunk:
                break
            for h in hashalg:
                m[h].update(chunk)
    return { h: m[h].hexdigest() for h in hashalg }


class IdxItem(object):

    def __init__(self, data=None, filename=None, basedir=None, hashalg=['md5']):
        self.filename = None
        self.tags = []
        if data is not None:
            # Compatibility with legacy index file formats.
            if 'md5' in data:
                data['checksum'] = {'md5': data['md5']}
                del data['md5']
            if 'createdate' in data:
                data['createDate'] = data['createdate']
                del data['createdate']
            self.__dict__.update(data)
        elif filename is not None:
            self.filename = filename
            if basedir is not None:
                filename = os.path.join(basedir, filename)
            self.checksum = _checksum(filename, hashalg)
            exifdata = Exif(filename)
            self.createDate = exifdata.createDate
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
