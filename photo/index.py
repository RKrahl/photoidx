"""Provide the class Index which represents an index of photos.
"""

import os
import os.path
import fnmatch
from collections import MutableSequence
import yaml
from photo.idxitem import IdxItem
from photo.listtools import LazyList


def _readdir(imgdir, basedir, hashalg, known=set()):
    for f in sorted(os.listdir(imgdir)):
        absfile = os.path.join(imgdir, f)
        f = os.path.relpath(absfile, basedir)
        if (os.path.isfile(absfile) and fnmatch.fnmatch(f, '*.jpg')
            and f not in known):
            yield IdxItem(filename=f, basedir=basedir, hashalg=hashalg)


class Index(MutableSequence):

    defIdxFilename = ".index.yaml"

    def __init__(self, idxfile=None, imgdir=None, hashalg=['md5']):
        super(Index, self).__init__()
        self.directory = None
        self.idxfilename = None
        self.items = []
        if idxfile:
            self.read(idxfile)
        if imgdir:
            imgdir = os.path.abspath(imgdir)
            if not self.directory:
                self.directory = imgdir
            if idxfile:
                known = { i.filename for i in self.items }
                newitems = _readdir(imgdir, self.directory, hashalg, known)
                self.items.extend(newitems)
            else:
                newitems = _readdir(imgdir, self.directory, hashalg)
                self.items = LazyList(newitems)

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

    def sort(self, key=None, reverse=None):
        self.items.sort(key, reverse)

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
            items = [i.as_dict() for i in sorted(self.items)]
            yaml.dump(items, f, default_flow_style=False)
