"""Filter image by various selection criteria.
"""

import datetime
import filecmp
import shutil
import pytest
import photoidx.index
import photoidx.idxfilter
from photoidx.geo import GeoPosition
from conftest import tmpdir, gettestdata

testimgs = [ 
    "dsc_4623.jpg", "dsc_4664.jpg", "dsc_4831.jpg", 
    "dsc_5126.jpg", "dsc_5167.jpg" 
]
testimgfiles = [ gettestdata(i) for i in testimgs ]

@pytest.fixture(scope="module")
def imgdir(tmpdir):
    for fname in testimgfiles:
        shutil.copy(fname, str(tmpdir))
    shutil.copy(gettestdata("index-tagged.yaml"), str(tmpdir / ".index.yaml"))
    return tmpdir

def test_by_date(imgdir):
    """Select by date.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        date = (datetime.datetime(2016, 3, 5), datetime.datetime(2016, 3, 6))
        idxfilter = photoidx.idxfilter.IdxFilter(date=date)
        fnames = [ str(i.filename) for i in idxfilter.filter(idx) ]
        assert fnames == ["dsc_4831.jpg"]

def test_by_gpspos(imgdir):
    """Select by GPS position.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        pos = GeoPosition("35.6883 N, 139.7544 E")
        idxfilter = photoidx.idxfilter.IdxFilter(gpspos=pos, gpsradius=20.0)
        fnames = [ str(i.filename) for i in idxfilter.filter(idx) ]
        assert fnames == ["dsc_4623.jpg", "dsc_4664.jpg"]

def test_by_files(imgdir):
    """Select by file names.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        files = ["dsc_4664.jpg", "dsc_4831.jpg"]
        idxfilter = photoidx.idxfilter.IdxFilter(files=files)
        fnames = [ str(i.filename) for i in idxfilter.filter(idx) ]
        assert fnames == files

def test_by_single_tag(imgdir):
    """Select by one single tag.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        idxfilter = photoidx.idxfilter.IdxFilter(tags="Shinto_shrine")
        fnames = [ str(i.filename) for i in idxfilter.filter(idx) ]
        assert fnames == ["dsc_4664.jpg", "dsc_4831.jpg"]

def test_by_mult_tags(imgdir):
    """Select by multiple tags.

    Combining multiple tags acts like an and, it selects only images
    having all the tags set.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        idxfilter = photoidx.idxfilter.IdxFilter(tags="Tokyo,Shinto_shrine")
        fnames = [ str(i.filename) for i in idxfilter.filter(idx) ]
        assert fnames == ["dsc_4664.jpg"]

def test_by_neg_tags(imgdir):
    """Select by negating tags.

    Prepending a tag by an exclamation mark selects the images having
    the tag not set.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        idxfilter = photoidx.idxfilter.IdxFilter(tags="Tokyo,!Shinto_shrine")
        fnames = [ str(i.filename) for i in idxfilter.filter(idx) ]
        assert fnames == ["dsc_4623.jpg"]

def test_by_empty_tag(imgdir):
    """Select by empty tags.

    The empty string as tag selects images having no tag.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        idxfilter = photoidx.idxfilter.IdxFilter(tags="")
        fnames = [ str(i.filename) for i in idxfilter.filter(idx) ]
        assert fnames == ["dsc_5126.jpg", "dsc_5167.jpg"]

def test_by_date_and_tag(imgdir):
    """Select by date and tags.

    Multiple selection criteria, such as date and tags may be
    combined.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        date = (datetime.datetime(2016, 2, 28), datetime.datetime(2016, 2, 29))
        idxfilter = photoidx.idxfilter.IdxFilter(tags="Tokyo", date=date)
        fnames = [ str(i.filename) for i in idxfilter.filter(idx) ]
        assert fnames == ["dsc_4623.jpg"]

def test_by_selected(imgdir):
    """Select by selected flag.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        idxfilter = photoidx.idxfilter.IdxFilter(select=True)
        fnames = [ str(i.filename) for i in idxfilter.filter(idx) ]
        assert fnames == ["dsc_4664.jpg", "dsc_5126.jpg"]

def test_by_selected_and_tag(imgdir):
    """Select by selected flag and tag.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        idxfilter = photoidx.idxfilter.IdxFilter(select=True, tags="Tokyo")
        fnames = [ str(i.filename) for i in idxfilter.filter(idx) ]
        assert fnames == ["dsc_4664.jpg"]

def test_by_not_selected(imgdir):
    """Select by not-selected flag.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        idxfilter = photoidx.idxfilter.IdxFilter(select=False)
        fnames = [ str(i.filename) for i in idxfilter.filter(idx) ]
        assert fnames == ["dsc_4623.jpg", "dsc_4831.jpg", "dsc_5167.jpg"]

