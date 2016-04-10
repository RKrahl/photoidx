"""Add images to an index.
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
else:
    refindex = gettestdata("index-create.yaml")

def test_createupdate(tmpdir):
    for fname in testimgfiles[:3]:
        shutil.copy(fname, tmpdir)
    idx = photo.index.Index(imgdir=tmpdir)
    idx.write()
    for fname in testimgfiles[3:]:
        shutil.copy(fname, tmpdir)
    idx = photo.index.Index(idxfile=tmpdir, imgdir=tmpdir)
    idx.write()
    idxfile = os.path.join(tmpdir, ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"
