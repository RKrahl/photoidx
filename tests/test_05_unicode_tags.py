"""Unwanted unicode marker for tags in the index.  (Issue #22)

When tags are set as unicode while the content is pure ASCII, PyYAML
marks them as `!!python/unicode 'tag'`.
"""

import os.path
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
baseindex = gettestdata("index-create.yaml")
refindex = gettestdata("index-unicode-tags.yaml")

tags = {
    "dsc_4623.jpg": [ u"T\u014Dky\u014D", u"Ginza" ],
    "dsc_4664.jpg": [ u"T\u014Dky\u014D", u"Meiji-jing\u016B", u"Shint\u014D" ],
    "dsc_4831.jpg": [ u"Hakone", u"Shint\u014D" ],
    "dsc_5126.jpg": [ u"Ky\u014Dto", u"Gion" ],
    "dsc_5167.jpg": [ u"Ky\u014Dto", u"Ry\u014Dan-ji", u"Buddha" ],
}


@pytest.fixture(scope="module")
def imgdir(tmpdir):
    for fname in testimgfiles:
        shutil.copy(fname, tmpdir)
    shutil.copy(baseindex, os.path.join(tmpdir, ".index.yaml"))
    return tmpdir

def test_tag_unicode(imgdir):
    with photo.index.Index(imgdir=imgdir) as idx:
        for item in idx:
            for t in tags[item.filename]:
                item.tags.add(t)
        idx.write()
    idxfile = os.path.join(imgdir, ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"
