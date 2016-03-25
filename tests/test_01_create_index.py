"""Create an image index.
"""

import os.path
import shutil
import filecmp
import pytest
import photo.index
from conftest import tmpdir, gettestdata, testimgs

refindex = gettestdata("index-create.yaml")

@pytest.fixture(scope="module")
def imgdir(tmpdir):
    for fname in testimgs:
        shutil.copy(gettestdata(fname), tmpdir)
    return tmpdir

def test_create(imgdir):
    idx = photo.index.Index(imgdir=imgdir)
    idx.write()
    idxfile = os.path.join(imgdir, ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"
