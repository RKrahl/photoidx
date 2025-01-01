"""Unwanted unicode marker for tags in the index.  (Issue #22)

When tags are set as unicode while the content is pure ASCII, PyYAML
marks them as `!!python/unicode 'tag'`.
"""

import shutil
import pytest
import photoidx.index
from conftest import tmpdir, gettestdata, index_cmp

testimgs = [ 
    "dsc_4623.jpg", "dsc_4664.jpg", "dsc_4831.jpg", 
    "dsc_5126.jpg", "dsc_5167.jpg" 
]
testimgfiles = [ gettestdata(i) for i in testimgs ]
baseindex = gettestdata("index.yaml")
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
        shutil.copy(fname, tmpdir)
    shutil.copy(baseindex, tmpdir / ".index.yaml")
    return tmpdir

def test_tag_unicode(imgdir):
    with photoidx.index.Index(imgdir=imgdir) as idx:
        for item in idx:
            for t in tags[str(item.filename)]:
                item.tags.add(t)
        idx.write()
    idxfile = imgdir / ".index.yaml"
    assert index_cmp(idxfile, refindex), "index file differs from reference"
