"""Read an image index from the index file and write it back.
"""

import os.path
import shutil
import filecmp
import pytest
import photo.index
from conftest import tmpdir, gettestdata

testimgs = [ 
    "dsc_4623.jpg", "dsc_4664.jpg", "dsc_4831.jpg", 
    "dsc_5126.jpg", "dsc_5167.jpg" 
]
testimgfiles = [ gettestdata(i) for i in testimgs ]

refindex = gettestdata("index-tagged.yaml")
refindexu = gettestdata("index-unicode-tags.yaml")

@pytest.fixture(scope="module")
def imgdir(tmpdir):
    for fname in testimgfiles:
        shutil.copy(fname, tmpdir)
    return tmpdir

def test_read_non_existent(imgdir):
    """Try to read an index file that does not exist.
    """
    with pytest.raises(IOError):
        with photo.index.Index(idxfile=imgdir) as idx:
            pass

def test_read_write(imgdir):
    """Read the index file and write it out again.
    """
    shutil.copy(refindex, os.path.join(imgdir, ".index.yaml"))
    with photo.index.Index(idxfile=imgdir) as idx:
        idx.write()
    idxfile = os.path.join(imgdir, ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"

def test_read_write_unicode(imgdir):
    """Same test as above but with non-ASCII characters in the tags.
    """
    shutil.copy(refindexu, os.path.join(imgdir, ".index.yaml"))
    with photo.index.Index(idxfile=imgdir) as idx:
        idx.write()
    idxfile = os.path.join(imgdir, ".index.yaml")
    assert filecmp.cmp(refindexu, idxfile), "index file differs from reference"
