"""Create an image index.
"""

import os.path
import datetime
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

if hasattr(datetime, "timezone"):
    refindex = gettestdata("index-create-tz.yaml")
    have_timezone = True
else:
    refindex = gettestdata("index-create.yaml")
    have_timezone = False

@pytest.fixture(scope="module")
def imgdir(tmpdir):
    for fname in testimgfiles:
        shutil.copy(fname, tmpdir)
    return tmpdir

def test_create(imgdir):
    """Create a new index adding all images in the imgdir.
    """
    idx = photo.index.Index(imgdir=imgdir)
    idx.write()
    idxfile = os.path.join(imgdir, ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"

@pytest.mark.xfail("have_timezone", 
                   reason="PyYAML fails to read datetime values with time zone")
def test_read(imgdir):
    """Read the index file and write it out again.
    """
    idx = photo.index.Index(idxfile=imgdir)
    idx.write()
    idxfile = os.path.join(imgdir, ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"
