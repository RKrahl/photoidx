"""Sort the image index.
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

@pytest.fixture(scope="module")
def imgdir(tmpdir):
    for fname in testimgfiles:
        shutil.copy(fname, tmpdir)
    shutil.copy(refindex, os.path.join(tmpdir, ".index.yaml"))
    return tmpdir

def test_sort_no_change(imgdir):
    """Do not modify any sort keys.  The order should not change.
    """
    idx = photo.index.Index(idxfile=imgdir)
    idx.sort()
    expected = [ 
        "dsc_4623.jpg", "dsc_4664.jpg", "dsc_4831.jpg",
        "dsc_5126.jpg", "dsc_5167.jpg"
    ]
    assert [ i.filename for i in idx ] == expected

def test_sort_change(imgdir):
    """Modify some sort keys.  The order should change accordingly.
    """
    idx = photo.index.Index(idxfile=imgdir)
    idx[1].sortkey = [ "xx" ]
    idx[3].sortkey = [ "xa" ]
    idx.sort()
    expected = [ 
        "dsc_4623.jpg", "dsc_4831.jpg", "dsc_5167.jpg",
        "dsc_5126.jpg", "dsc_4664.jpg"
    ]
    assert [ i.filename for i in idx ] == expected
