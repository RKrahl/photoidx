"""Provide the class Index which represents an index of photos.
"""

from collections.abc import MutableSequence
import datetime
import errno
import fcntl
import os
from pathlib import Path
from packaging.version import Version
import yaml
from .idxitem import IdxItem
from .listtools import LazyList


class AlreadyLockedError(OSError):
    def __init__(self, *args):
        super().__init__(*args)


class Index(MutableSequence):

    idxFileVersion = "2.0"
    defIdxFilename = Path(".index.yaml")

    def _readdir(self, imgdir, known=set()):
        for f in sorted(imgdir.iterdir()):
            rel = f.relative_to(self.directory)
            if f.is_file() and f.suffix == '.jpg' and rel not in known:
                yield IdxItem(self, filename=rel)

    def _get_common_checksums(self):
        if len(self.items):
            checksums = set(self.items[0].checksum.keys())
            for i in self.items:
                checksums.intersection(i.checksum.keys())
            return list(checksums)
        else:
            return self.checksums

    def __init__(self, idxfile=None, imgdir=None,
                 checksums=['md5'], comment=None):
        super().__init__()
        self.head = dict(Checksums=checksums)
        self.directory = None
        self.idxfile = None
        self.items = []
        if idxfile:
            self.read(idxfile)
        if comment:
            self.head['Comment'] = comment
        if imgdir:
            imgdir = Path(imgdir).resolve()
            if not self.directory:
                self.directory = imgdir
            if idxfile:
                self.extend_dir(imgdir)
            else:
                newitems = self._readdir(imgdir)
                self.items = LazyList(newitems)

    @property
    def version(self):
        v = self.head.get("Version")
        if v is not None:
            return Version(v)

    @property
    def date(self):
        return self.head.get("Date")

    @property
    def comment(self):
        return self.head.get("Comment")

    @property
    def timeZone(self):
        return self.head.get("TimeZone")

    @property
    def checksums(self):
        return self.head.get("Checksums")

    def extend_dir(self, imgdir):
        imgdir = Path(imgdir).resolve()
        known = { i.filename for i in self.items }
        newitems = self._readdir(imgdir, known)
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

    def _get_idxfile(self, fname, flags):
        if fname is not None:
            self.close()
            fname = Path(fname)
            if fname.is_dir():
                fname = fname / self.defIdxFilename
            self.directory = fname.parent.resolve()
            fd = os.open(str(fname), flags, mode=0o666)
            self.idxfile = os.fdopen(fd, "r+t")
        elif self.idxfile:
            self.idxfile.seek(0)
        else:
            if not self.directory:
                self.directory = Path.cwd()
            fname = self.directory / self.defIdxFilename
            fd = os.open(str(fname), flags, mode=0o666)
            self.idxfile = os.fdopen(fd, "r+t")

    def _lockf(self, mode=fcntl.LOCK_SH):
        try:
            fcntl.lockf(self.idxfile.fileno(), mode | fcntl.LOCK_NB)
        except OSError as e:
            if e.errno in (errno.EACCES, errno.EAGAIN):
                e = AlreadyLockedError(*e.args)
            raise e

    def read(self, idxfile=None):
        """Read the index from a file.
        """
        self._get_idxfile(idxfile, os.O_RDWR)
        self._lockf()
        docs = yaml.safe_load_all(self.idxfile)
        head = next(docs)
        try:
            items = next(docs)
        except StopIteration:
            # Legacy index file
            self.items = [ IdxItem(self, data=i) for i in head ]
            self.head = {
                'Version': "1.0",
                'Date': None,
                'TimeZone': None,
                'Checksums': self._get_common_checksums(),
            }
        else:
            self.head = head
            self.items = [ IdxItem(self, data=i) for i in items ]

    def write(self, idxfile=None):
        """Write the index to a file.
        """
        head = {
            'Version': self.idxFileVersion,
            'Date': datetime.datetime.now(tz=self.timeZone),
            'TimeZone': self.timeZone,
            'Checksums': self.checksums,
        }
        if self.comment:
            head['Comment'] = self.comment
        items = [ i.as_dict() for i in self.items ]
        self._get_idxfile(idxfile, os.O_RDWR|os.O_CREAT)
        self._lockf(mode=fcntl.LOCK_EX)
        self.idxfile.write("%YAML 1.1\n")
        yaml.dump(head, self.idxfile,
                  default_flow_style=False, explicit_start=True)
        yaml.dump(items, self.idxfile,
                  default_flow_style=False, explicit_start=True)
        self.idxfile.truncate()
        self.idxfile.flush()
        self._lockf()

