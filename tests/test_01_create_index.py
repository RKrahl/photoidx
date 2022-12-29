"""Create an image index.
"""

import filecmp
import shutil
import pytest
import photoidx.index
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
        shutil.copy(fname, str(tmpdir))
    return tmpdir

def test_create_curdir(imgdir, monkeypatch):
    """Create a new index in the current directory adding all images.
    """
    monkeypatch.chdir(str(imgdir))
    with photoidx.index.Index(imgdir=".") as idx:
        idx.write()
    idxfile = ".index.yaml"
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"

@pytest.mark.dependency()
def test_create(imgdir):
    """Create a new index adding all images in the imgdir.
    """
    with photoidx.index.Index(imgdir=imgdir) as idx:
        idx.write()
    idxfile = str(imgdir / ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"

@pytest.mark.dependency(depends=["test_create"])
def test_read(imgdir):
    """Read the index file and write it out again.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        idx.write()
    idxfile = str(imgdir / ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"
