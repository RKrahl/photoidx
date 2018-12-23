"""Filter image by various selection criteria.
"""

import os.path
import shutil
import filecmp
import datetime
import pytest
import photo.index
import photo.idxfilter
from conftest import tmpdir, gettestdata

testimgs = [ 
    "dsc_4623.jpg", "dsc_4664.jpg", "dsc_4831.jpg", 
    "dsc_5126.jpg", "dsc_5167.jpg" 
]
testimgfiles = [ gettestdata(i) for i in testimgs ]

@pytest.fixture(scope="module")
def imgdir(tmpdir):
    for fname in testimgfiles:
        shutil.copy(fname, tmpdir)
    shutil.copy(gettestdata("index-tagged.yaml"), 
                os.path.join(tmpdir, ".index.yaml"))
    return tmpdir

def test_by_date(imgdir):
    """Select by date.
    """
    idx = photo.index.Index(idxfile=imgdir)
    idxfilter = photo.idxfilter.IdxFilter(date="2016-03-05")
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4831.jpg"]

def test_by_gpspos(imgdir):
    """Select by GPS position.
    """
    idx = photo.index.Index(idxfile=imgdir)
    idxfilter = photo.idxfilter.IdxFilter(gpspos="35.6883 N, 139.7544 E", 
                                          gpsradius=20.0)
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4623.jpg", "dsc_4664.jpg"]

def test_by_files(imgdir):
    """Select by file names.
    """
    idx = photo.index.Index(idxfile=imgdir)
    idxfilter = photo.idxfilter.IdxFilter(files=["dsc_4664.jpg", 
                                                 "dsc_4831.jpg"])
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4664.jpg", "dsc_4831.jpg"]

def test_by_single_tag(imgdir):
    """Select by one single tag.
    """
    idx = photo.index.Index(idxfile=imgdir)
    idxfilter = photo.idxfilter.IdxFilter(tags="Shinto_shrine")
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4664.jpg", "dsc_4831.jpg"]

def test_by_mult_tags(imgdir):
    """Select by multiple tags.

    Combining multiple tags acts like an and, it selects only images
    having all the tags set.
    """
    idx = photo.index.Index(idxfile=imgdir)
    idxfilter = photo.idxfilter.IdxFilter(tags="Tokyo,Shinto_shrine")
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4664.jpg"]

def test_by_neg_tags(imgdir):
    """Select by negating tags.

    Prepending a tag by an exclamation mark selects the images having
    the tag not set.
    """
    idx = photo.index.Index(idxfile=imgdir)
    idxfilter = photo.idxfilter.IdxFilter(tags="Tokyo,!Shinto_shrine")
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4623.jpg"]

def test_by_empty_tag(imgdir):
    """Select by empty tags.

    The empty string as tag selects images having no tag.
    """
    idx = photo.index.Index(idxfile=imgdir)
    idxfilter = photo.idxfilter.IdxFilter(tags="")
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_5126.jpg", "dsc_5167.jpg"]

def test_by_date_and_tag(imgdir):
    """Select by date and tags.

    Multiple selection criteria, such as date and tags may be
    combined.
    """
    idx = photo.index.Index(idxfile=imgdir)
    idxfilter = photo.idxfilter.IdxFilter(tags="Tokyo", date="2016-02-28")
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4623.jpg"]

def test_by_selected(imgdir):
    """Select by selected flag.
    """
    idx = photo.index.Index(idxfile=imgdir)
    idxfilter = photo.idxfilter.IdxFilter(select=True)
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4664.jpg", "dsc_5126.jpg"]

def test_by_selected_and_tag(imgdir):
    """Select by selected flag and tag.
    """
    idx = photo.index.Index(idxfile=imgdir)
    idxfilter = photo.idxfilter.IdxFilter(select=True, tags="Tokyo")
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4664.jpg"]

def test_by_not_selected(imgdir):
    """Select by not-selected flag.
    """
    idx = photo.index.Index(idxfile=imgdir)
    idxfilter = photo.idxfilter.IdxFilter(select=False)
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4623.jpg", "dsc_4831.jpg", "dsc_5167.jpg"]

