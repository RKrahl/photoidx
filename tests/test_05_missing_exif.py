"""Handle missing exif tags gracefully.  (Issue #15)

When creating a new index, the constructor of class IdxItem reads some
exif tags like DateTimeOriginal and Orientaion from the images to add
the information to the index.  But it should not raise an error if
some exif tags are missing.
"""

import shutil
import pytest
import photoidx.index
from conftest import tmpdir, gettestdata

testimgs = [ 
    "dsc_1190.jpg", "dsc_4623.jpg", "dsc_4664.jpg", 
    "dsc_4831.jpg", "dsc_5126.jpg", "dsc_5167.jpg" 
]
testimgfiles = [ gettestdata(i) for i in testimgs ]

@pytest.fixture(scope="module")
def imgdir(tmpdir):
    for fname in testimgfiles:
        shutil.copy(fname, str(tmpdir))
    return tmpdir

def test_create(imgdir):
    with photoidx.index.Index(imgdir=imgdir) as idx:
        idx.write()
