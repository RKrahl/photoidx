"""Create an image index.
"""

from pathlib import Path
import shutil
import pytest
from photoidx.datetools import gettz
import photoidx.index
from conftest import tmpdir, gettestdata, index_cmp

testimgs = [ 
    "dsc_4623.jpg", "dsc_4664.jpg", "dsc_4831.jpg", 
    "dsc_5126.jpg", "dsc_5167.jpg" 
]
testimgfiles = [ gettestdata(i) for i in testimgs ]

refindex = gettestdata("index.yaml")

@pytest.fixture(scope="module")
def imgdir(tmpdir):
    for fname in testimgfiles:
        shutil.copy(fname, tmpdir)
    return tmpdir

def test_create_curdir(imgdir, monkeypatch):
    """Create a new index in the current directory adding all images.
    """
    monkeypatch.chdir(imgdir)
    with photoidx.index.Index(imgdir=".", comment="Japan 2016",
                              default_tz=gettz("Asia/Tokyo")) as idx:
        idx.write()
    idxfile = Path(".index.yaml")
    assert index_cmp(idxfile, refindex), "index file differs from reference"

@pytest.mark.dependency()
def test_create(imgdir):
    """Create a new index adding all images in the imgdir.
    """
    with photoidx.index.Index(imgdir=imgdir, comment="Japan 2016",
                              default_tz=gettz("Asia/Tokyo")) as idx:
        idx.write()
    idxfile = imgdir / ".index.yaml"
    assert index_cmp(idxfile, refindex), "index file differs from reference"

@pytest.mark.dependency(depends=["test_create"])
def test_read(imgdir):
    """Read the index file and write it out again.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        idx.write()
    idxfile = imgdir / ".index.yaml"
    assert index_cmp(idxfile, refindex), "index file differs from reference"
