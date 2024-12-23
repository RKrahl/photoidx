"""Provide the class IdxItem which represents an item in the index.
"""

import datetime
import hashlib
from pathlib import Path
from .exif import Orientation, Exif
from .geo import GeoPosition


def _checksum(fname, hashalg):
    """Calculate hashes for a file.
    """
    if not hashalg:
        return {}
    m = { h:hashlib.new(h) for h in hashalg }
    chunksize = 8192
    with fname.open('rb') as f:
        while True:
            chunk = f.read(chunksize)
            if not chunk:
                break
            for h in hashalg:
                m[h].update(chunk)
    return { h: m[h].hexdigest() for h in hashalg }


class IdxItem(object):

    def __init__(self, data=None, filename=None, basedir=None,
                 hashalg=['md5'], default_tz=None):
        self.exifdata = None
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
            if basedir is not None:
                filename = Path(basedir) / filename
            self.checksum = _checksum(filename, hashalg)
            self.exifdata = Exif(filename)
            self.createDate = self.exifdata.createDate
            self.orientation = self.exifdata.orientation
            self.gpsPosition = self.exifdata.gpsPosition
            tzinfo = self.get_createDate_tzinfo(fallback=default_tz)
            self.createDate = self.createDate.replace(tzinfo=tzinfo)
            self.tags = set()
            self.selected = False
        if self.gpsPosition:
            self.gpsPosition = GeoPosition(self.gpsPosition)

    def get_createDate_tzinfo(self, fallback=None):
        """Get time zone info from createDate.

        If createDate is naive, e.g. does not have time zone
        information, try to derive that information from other
        attributes.
        """
        if self.createDate.tzinfo:
            return self.createDate.tzinfo
        if self.exifdata and self.exifdata.gpsDateTime:
            # Assume gpsDateTime to be UTC and use the offset between
            # createDate and gpsDateTime to generate time zone info.
            offs = self.createDate - self.exifdata.gpsDateTime
            return datetime.timezone(offs)
        # No luck, return fallback.
        return fallback

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
