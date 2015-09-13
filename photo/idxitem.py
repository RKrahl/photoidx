"""Provide the class IdxItem which represents an item in the index.
"""

import hashlib


def _md5file(fname):
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
    return m.hexdigest()


class IdxItem(object):

    def __init__(self, filename=None, data=None):
        self.filename = None
        self.tags = []
        if data is not None:
            self.__dict__.update(data)
        elif filename is not None:
            self.filename = filename
            self.md5 = _md5file(filename)
        self.tags = set(self.tags)

    def as_dict(self):
        d = self.__dict__.copy()
        d['tags'] = list(d['tags'])
        return d
