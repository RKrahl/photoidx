"""Read legacy format index files.

Since version 0.4 different checksum algorithms are supported (Issue
#12).  As a consequence, the index file format is changed.
photo-tools still reads legacy files and transparently converts them
to the new format.  This feature is tested in this module.
"""

import filecmp
import shutil
import pytest
import photo.index
from conftest import tmpdir, gettestdata

testimgs = [ 
    "dsc_4623.jpg", "dsc_4664.jpg", "dsc_4831.jpg", 
    "dsc_5126.jpg", "dsc_5167.jpg" 
]
testimgfiles = [ gettestdata(i) for i in testimgs ]

legacyindex = gettestdata("index-legacy.yaml")
refindex = gettestdata("index-create.yaml")

def test_legacyconvert(tmpdir):
    for fname in testimgfiles:
        shutil.copy(fname, str(tmpdir))
    idxfile = str(tmpdir.joinpath(".index.yaml"))
    shutil.copy(legacyindex, idxfile)
    # reading and writing the index transparantly converts it.
    with photo.index.Index(idxfile=tmpdir) as idx:
        idx.write()
    assert filecmp.cmp(idxfile, refindex), "index file differs from reference"
