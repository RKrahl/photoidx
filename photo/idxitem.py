"""Provide the class IdxItem which represents an item in the index.
"""

import os.path
import hashlib
from photo.exif import Exif
from photo.geo import GeoPosition


def _checksum(fname, hashalg):
    """Calculate hashes for a file.
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
        if data is not None:
            self.filename = data.get('filename')
            self.name = data.get('name', None)
            self.checksum = data.get('checksum', {})
            if not self.checksum and 'md5' in data:
                # legacy: old index file format used to have a 'md5'
                # attribute, rather then 'checksum'.
                self.checksum['md5'] = data['md5']
            self.createDate = data.get('createDate')
            if self.createDate is None and 'createdate' in data:
                # legacy: 'createDate' used to be 'createdate' in old
                # index file format.
                self.createDate = data['createdate']
            self.orientation = data.get('orientation')
            self.gpsPosition = data.get('gpsPosition')
            tags = data.get('tags', [])
            self.tags = set(filter(lambda t: not t.startswith('pidx:'), tags))
            self.selected = 'pidx:selected' in tags
            self.sortkey = data.get('sortkey')
        elif filename is not None:
            self.filename = filename
            self.name = None
            if basedir is not None:
                filename = os.path.join(basedir, filename)
            self.checksum = _checksum(filename, hashalg)
            exifdata = Exif(filename)
            self.createDate = exifdata.createDate
            self.orientation = exifdata.orientation
            self.gpsPosition = exifdata.gpsPosition
            self.tags = set()
            self.selected = False
            self.sortkey = None
        if self.gpsPosition:
            self.gpsPosition = GeoPosition(self.gpsPosition)
        if self.sortkey is None:
            try:
                self.sortkey = [self.createDate.isoformat()]
            except AttributeError:
                self.sortkey = []

    def as_dict(self):
        tags = self.tags.copy()
        if self.selected:
             tags.add('pidx:selected')
        d = {
            'filename': self.filename,
            'checksum': self.checksum,
            'createDate': self.createDate,
            'orientation': self.orientation,
            'gpsPosition': self.gpsPosition,
            'tags': sorted(tags),
            'sortkey': self.sortkey,
        }
        if d['gpsPosition']:
            d['gpsPosition'] = d['gpsPosition'].as_dict()
        if self.name is not None:
            d['name'] = self.name
        return d

    def __lt__(self, other):
        if isinstance(other, IdxItem):
            return self.sortkey < other.sortkey
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, IdxItem):
            return self.sortkey > other.sortkey
        else:
            return NotImplemented
