"""Read legacy format index files.

Since version 0.4 different checksum algorithms are supported (Issue
#12).  As a consequence, the index file format is changed.
photo-tools still reads legacy files and transparently converts them
to the new format.  This feature is tested in this module.
"""

import os.path
import shutil
import filecmp
import pytest
import photo.index
from conftest import tmpdir, gettestdata, testimgs

legacyindex = gettestdata("index-legacy.yaml")
refindex = gettestdata("index-create.yaml")

def test_legacyconvert(tmpdir):
    for fname in testimgs:
        shutil.copy(gettestdata(fname), tmpdir)
    idxfile = os.path.join(tmpdir, ".index.yaml")
    shutil.copy(legacyindex, idxfile)
    # reading and writing the index transparantly converts it.
    idx = photo.index.Index(idxfile=tmpdir)
    idx.write()
    assert filecmp.cmp(idxfile, refindex), "index file differs from reference"
