"""Add images to an index.
"""

import os.path
import shutil
import filecmp
import pytest
import photo.index
from conftest import tmpdir, gettestdata, testimgs

refindex = gettestdata("index-create.yaml")

def test_createupdate(tmpdir):
    for fname in testimgs[:3]:
        shutil.copy(gettestdata(fname), tmpdir)
    idx = photo.index.Index(imgdir=tmpdir)
    idx.write()
    for fname in testimgs[3:]:
        shutil.copy(gettestdata(fname), tmpdir)
    idx = photo.index.Index(idxfile=tmpdir, imgdir=tmpdir)
    idx.write()
    idxfile = os.path.join(tmpdir, ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"
