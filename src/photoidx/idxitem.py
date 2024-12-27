"""Provide the class IdxItem which represents an item in the index.
"""

import hashlib
from pathlib import Path
from .exif import Orientation, Exif
from .geo import GeoPosition


def _checksum(fname, checksums):
    """Calculate hashes for a file.
    """
    if not checksums:
        return {}
    m = { h:hashlib.new(h) for h in checksums }
    chunksize = 8192
    with fname.open('rb') as f:
        while True:
            chunk = f.read(chunksize)
            if not chunk:
                break
            for h in checksums:
                m[h].update(chunk)
    return { h: m[h].hexdigest() for h in checksums }


class IdxItem(object):

    def __init__(self, index, data=None, filename=None, checksums=['md5']):
        if data is not None:
            self.filename = Path(data.get('filename'))
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
            self.orientation = Orientation(data.get('orientation'))
            self.gpsPosition = data.get('gpsPosition')
            tags = data.get('tags', [])
            self.tags = set(filter(lambda t: not t.startswith('pidx:'), tags))
            self.selected = 'pidx:selected' in tags
        elif filename is not None:
            filename = Path(filename)
            self.filename = filename
            self.name = None
            if index.directory is not None:
                filename = index.directory / filename
            self.checksum = _checksum(filename, checksums)
            exifdata = Exif(filename)
            self.createDate = exifdata.createDate
            self.orientation = exifdata.orientation
            self.gpsPosition = exifdata.gpsPosition
            self.tags = set()
            self.selected = False
        if self.gpsPosition:
            self.gpsPosition = GeoPosition(self.gpsPosition)

    def as_dict(self):
        tags = self.tags.copy()
        if self.selected:
             tags.add('pidx:selected')
        d = {
            'filename': str(self.filename),
            'checksum': self.checksum,
            'createDate': self.createDate,
            'orientation': str(self.orientation) if self.orientation else None,
            'gpsPosition': self.gpsPosition,
            'tags': sorted(tags),
        }
        if d['gpsPosition']:
            d['gpsPosition'] = d['gpsPosition'].as_dict()
        if self.name is not None:
            d['name'] = self.name
        return d
