"""Unwanted unicode marker for tags in the index.  (Issue #22)

When tags are set as unicode while the content is pure ASCII, PyYAML
marks them as `!!python/unicode 'tag'`.
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
baseindex = gettestdata("index-create.yaml")
refindex = gettestdata("index-unicode-tags.yaml")

tags = {
    "dsc_4623.jpg": [ "T\u014Dky\u014D", "Ginza" ],
    "dsc_4664.jpg": [ "T\u014Dky\u014D", "Meiji-jing\u016B", "Shint\u014D" ],
    "dsc_4831.jpg": [ "Hakone", "Shint\u014D" ],
    "dsc_5126.jpg": [ "Ky\u014Dto", "Gion" ],
    "dsc_5167.jpg": [ "Ky\u014Dto", "Ry\u014Dan-ji", "Buddha" ],
}


@pytest.fixture(scope="module")
def imgdir(tmpdir):
    for fname in testimgfiles:
        shutil.copy(fname, str(tmpdir))
    shutil.copy(baseindex, str(tmpdir / ".index.yaml"))
    return tmpdir

def test_tag_unicode(imgdir):
    with photoidx.index.Index(imgdir=imgdir) as idx:
        for item in idx:
            for t in tags[str(item.filename)]:
                item.tags.add(t)
        idx.write()
    idxfile = str(imgdir / ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"
