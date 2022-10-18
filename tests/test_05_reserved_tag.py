"""Filter reserved tags on reading an index.

The prefix 'pidx:' for tags is reserved for internal use in photoidx.
It should be removed when reading an index file.
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

invindex = gettestdata("index-reserved-tags.yaml")
refindex = gettestdata("index-tagged.yaml")

def test_reserved_tags_convert(tmpdir):
    for fname in testimgfiles:
        shutil.copy(fname, str(tmpdir))
    idxfile = str(tmpdir / ".index.yaml")
    shutil.copy(invindex, idxfile)
    # reading and writing the index transparantly filters out tags
    # using the reserved prefix.
    with photoidx.index.Index(idxfile=tmpdir) as idx:
        idx.write()
    assert filecmp.cmp(idxfile, refindex), "index file differs from reference"
