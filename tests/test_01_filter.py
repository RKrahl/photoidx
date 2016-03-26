"""Filter image by various selection criteria.
"""

import os.path
import shutil
import filecmp
import datetime
import pytest
import photo.index
import photo.idxfilter
from conftest import tmpdir, gettestdata, testimgs


@pytest.fixture(scope="module")
def imgdir(tmpdir):
    for fname in testimgs:
        shutil.copy(gettestdata(fname), tmpdir)
    shutil.copy(gettestdata("index-create.yaml"), 
                os.path.join(tmpdir, ".index.yaml"))
    return tmpdir

class NameSpace(object):
    def __init__(self, **kwargs):
        for k in ["tags", "date", "gpspos", "gpsradius", "files"]:
            setattr(self, k, None)
        for k in kwargs:
            setattr(self, k, kwargs[k])

# Note: We need images to be tagged in order to test selection by tags
# in test_by_single_tag, test_by_mult_tags, test_by_neg_tags,
# test_by_empty_tag, and test_by_date_and_tag.  To this end
# test_by_date, test_by_gpspos, and test_by_files add tags to the
# images as a side effect.

def test_by_date(imgdir):
    """Select by date.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = NameSpace(date=datetime.date(2016, 3, 5))
    idxfilter = photo.idxfilter.IdxFilter(args)
    fnames = []
    for i in filter(idxfilter, idx):
        fnames.append(i.filename)
        i.tags.add("Hakone")
    assert fnames == ["dsc_4831.jpg"]
    idx.write()

def test_by_gpspos(imgdir):
    """Select by GPS position.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = NameSpace(gpspos="35.6883 N, 139.7544 E", gpsradius=20.0)
    idxfilter = photo.idxfilter.IdxFilter(args)
    fnames = []
    for i in filter(idxfilter, idx):
        fnames.append(i.filename)
        i.tags.add("Tokyo")
    assert fnames == ["dsc_4623.jpg", "dsc_4664.jpg"]
    idx.write()

def test_by_files(imgdir):
    """Select by file names.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = NameSpace(files=["dsc_4664.jpg", "dsc_4831.jpg"])
    idxfilter = photo.idxfilter.IdxFilter(args)
    fnames = []
    for i in filter(idxfilter, idx):
        fnames.append(i.filename)
        i.tags.add("Shinto_shrine")
    assert fnames == ["dsc_4664.jpg", "dsc_4831.jpg"]
    idx.write()

def test_by_single_tag(imgdir):
    """Select by one single tag.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = NameSpace(tags="Shinto_shrine")
    idxfilter = photo.idxfilter.IdxFilter(args)
    fnames = [ i.filename for i in filter(idxfilter, idx) ]
    assert fnames == ["dsc_4664.jpg", "dsc_4831.jpg"]

def test_by_mult_tags(imgdir):
    """Select by multiple tags.

    Combining multiple tags acts like an and, it selects only images
    having all the tags set.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = NameSpace(tags="Tokyo,Shinto_shrine")
    idxfilter = photo.idxfilter.IdxFilter(args)
    fnames = [ i.filename for i in filter(idxfilter, idx) ]
    assert fnames == ["dsc_4664.jpg"]

def test_by_neg_tags(imgdir):
    """Select by tags.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = NameSpace(tags="Tokyo,!Shinto_shrine")
    idxfilter = photo.idxfilter.IdxFilter(args)
    fnames = [ i.filename for i in filter(idxfilter, idx) ]
    assert fnames == ["dsc_4623.jpg"]

def test_by_empty_tag(imgdir):
    """Select by negating tags.

    Prepending a tag by an exclamation mark selects the images having
    the tag not set.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = NameSpace(tags="")
    idxfilter = photo.idxfilter.IdxFilter(args)
    fnames = [ i.filename for i in filter(idxfilter, idx) ]
    assert fnames == ["dsc_5126.jpg", "dsc_5167.jpg"]

def test_by_date_and_tag(imgdir):
    """Select by date and tags.

    Multiple selection criteria, such as date and tags may be
    combined.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = NameSpace(tags="Tokyo", date=datetime.date(2016, 2, 28))
    idxfilter = photo.idxfilter.IdxFilter(args)
    fnames = [ i.filename for i in filter(idxfilter, idx) ]
    assert fnames == ["dsc_4623.jpg"]

