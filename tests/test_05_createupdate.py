"""Add images to an index.
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

def test_createupdate(tmpdir):
    for fname in testimgfiles[:3]:
        shutil.copy(fname, str(tmpdir))
    with photoidx.index.Index(imgdir=tmpdir) as idx:
        idx.write()
    for fname in testimgfiles[3:]:
        shutil.copy(fname, str(tmpdir))
    with photoidx.index.Index(idxfile=tmpdir, imgdir=tmpdir) as idx:
        idx.write()
    idxfile = str(tmpdir / ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"
