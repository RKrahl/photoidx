"""Provide the class Index which represents an index of photos.
"""

import os
import os.path
import fnmatch
from collections import MutableSequence
import yaml
from photo.idxitem import IdxItem
from photo.helper import tmpchdir


class Index(MutableSequence):

    defIdxFilename = ".index.yaml"

    def __init__(self, idxfile=None, imgdir=None):
        super(Index, self).__init__()
        self.directory = None
        self.idxfilename = None
        self.items = []
        if idxfile:
            self.read(idxfile)
        elif imgdir:
            self.readdir(imgdir)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items.__getitem__(index)

    def __setitem__(self, index, value):
        self.items.__setitem__(index, value)

    def __delitem__(self, index):
        self.items.__delitem__(index)

    def insert(self, index, value):
        self.items.insert(index, value)

    def _idxfilename(self, idxfile):
        """Determine the index file name for reading and writing.
        """
        if idxfile is not None:
            idxfile = os.path.abspath(idxfile)
            if os.path.isdir(idxfile):
                idxfile = os.path.join(idxfile, self.defIdxFilename)
            return idxfile
        elif self.idxfilename is not None:
            return self.idxfilename
        else:
            d = self.directory if self.directory is not None else os.getcwd()
            return os.path.abspath(os.path.join(d, self.defIdxFilename))

    def readdir(self, imgdir):
        """Create a new index of all image files in a directory.
        """
        self.directory = os.path.abspath(imgdir)
        self.items = []
        with tmpchdir(self.directory):
            for f in sorted(os.listdir(self.directory)):
                if (os.path.isfile(f) and fnmatch.fnmatch(f, '*.jpg')):
                    self.items.append(IdxItem(filename=f))

    def read(self, idxfile=None):
        """Read the index from a file.
        """
        self.idxfilename = self._idxfilename(idxfile)
        self.directory = os.path.dirname(self.idxfilename)
        with open(self.idxfilename, 'rt') as f:
            self.items = [IdxItem(data=i) for i in yaml.load(f)]

    def write(self, idxfile=None):
        """Write the index to a file.
        """
        with open(self._idxfilename(idxfile), 'wt') as f:
            items = [i.as_dict() for i in self.items]
            yaml.dump(items, f, default_flow_style=False)

    def filtered(self, f):
        """Return a filtered version of the index.
        """
        return filter(f, self.items)


class IndexFilter(object):
    """A filter to be passed to Index.filtered().
    """

    def __init__(self, taglist=None, negtaglist=None, date=None, filelist=None):
        self.taglist = set(taglist) if taglist is not None else None
        self.negtaglist = set(negtaglist) if negtaglist is not None else None
        self.date = date
        self.filelist = set(filelist) if filelist else None

    def __call__(self, item):
        if self.filelist and not item.filename in self.filelist:
            return False
        if self.taglist is not None:
            if not self.taglist <= item.tags:
                return False
            if not self.taglist and not self.negtaglist and item.tags:
                return False
        if self.negtaglist is not None:
            if self.negtaglist & item.tags:
                return False
        if self.date and item.createdate.date() != self.date:
            return False
        return True
