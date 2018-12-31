"""Provide the class Index which represents an index of photos.
"""

from collections import MutableSequence
import errno
import fcntl
import fnmatch
import os
import os.path
import yaml
from photo.idxitem import IdxItem
from photo.listtools import LazyList


class AlreadyLockedError(OSError):
    def __init__(self, *args):
        super(AlreadyLockedError, self).__init__(*args)


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
        self.idxfile = None
        self.items = []
        if idxfile:
            self.read(idxfile)
        if imgdir:
            imgdir = os.path.abspath(imgdir)
            if not self.directory:
                self.directory = imgdir
            if idxfile:
                self.extend_dir(imgdir, hashalg)
            else:
                newitems = _readdir(imgdir, self.directory, hashalg)
                self.items = LazyList(newitems)

    def extend_dir(self, imgdir, hashalg=['md5']):
        known = { i.filename for i in self.items }
        newitems = _readdir(imgdir, self.directory, hashalg, known)
        self.items.extend(newitems)

    def close(self):
        if self.idxfile:
            self.idxfile.close()
            self.idxfile = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def __del__(self):
        self.close()

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items.__getitem__(index)

    def __setitem__(self, index, value):
        self.items.__setitem__(index, value)

    def __delitem__(self, index):
        self.items.__delitem__(index)

    def index(self, value, *args):
        return self.items.index(value, *args)

    def insert(self, index, value):
        self.items.insert(index, value)

    def _get_idxfile(self, fname):
        if fname is not None:
            self.close()
            fname = os.path.abspath(fname)
            if os.path.isdir(fname):
                fname = os.path.join(fname, self.defIdxFilename)
            self.directory = os.path.dirname(fname)
            fd = os.open(fname, os.O_RDWR|os.O_CREAT)
            self.idxfile = os.fdopen(fd, "r+t")
        elif self.idxfile:
            self.idxfile.seek(0)
        else:
            if not self.directory:
                self.directory = os.getcwd()
            fname = os.path.join(self.directory, self.defIdxFilename)
            fd = os.open(fname, os.O_RDWR|os.O_CREAT)
            self.idxfile = os.fdopen(fd, "r+t")

    def _lockf(self, mode=fcntl.LOCK_SH):
        try:
            fcntl.lockf(self.idxfile.fileno(), mode | fcntl.LOCK_NB)
        except Exception as e:
            if (isinstance(e, (OSError, IOError)) and 
                e.errno in [errno.EACCES, errno.EAGAIN]):
                e = AlreadyLockedError(*e.args)
            raise e

    def read(self, idxfile=None):
        """Read the index from a file.
        """
        self._get_idxfile(idxfile)
        self._lockf()
        self.items = [ IdxItem(data=i) for i in yaml.load(self.idxfile) ]

    def write(self, idxfile=None):
        """Write the index to a file.
        """
        items = [ i.as_dict() for i in self.items ]
        self._get_idxfile(idxfile)
        self._lockf(mode=fcntl.LOCK_EX)
        yaml.dump(items, self.idxfile, default_flow_style=False)
        self.idxfile.truncate()
        self.idxfile.flush()
        self._lockf()

