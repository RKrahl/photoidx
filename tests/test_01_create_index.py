"""Create an image index.
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

refindex = gettestdata("index-create.yaml")

@pytest.fixture(scope="module")
def imgdir(tmpdir):
    for fname in testimgfiles:
        shutil.copy(fname, tmpdir)
    return tmpdir

def test_create_curdir(imgdir, monkeypatch):
    """Create a new index in the current directory adding all images.
    """
    monkeypatch.chdir(imgdir)
    idx = photo.index.Index(imgdir=".")
    idx.write()
    idxfile = ".index.yaml"
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"

def test_create(imgdir):
    """Create a new index adding all images in the imgdir.
    """
    idx = photo.index.Index(imgdir=imgdir)
    idx.write()
    idxfile = os.path.join(imgdir, ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"

def test_read(imgdir):
    """Read the index file and write it out again.
    """
    idx = photo.index.Index(idxfile=imgdir)
    idx.write()
    idxfile = os.path.join(imgdir, ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"
