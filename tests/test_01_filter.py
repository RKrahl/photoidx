"""Filter image by various selection criteria.
"""

import os.path
import argparse
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

@pytest.fixture(scope="module")
def argparser():
    parser = argparse.ArgumentParser()
    photo.idxfilter.addFilterArguments(parser)
    return parser

def test_by_date(imgdir, argparser):
    """Select by date.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = argparser.parse_args(["--date=2016-03-05"])
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4831.jpg"]

def test_by_gpspos(imgdir, argparser):
    """Select by GPS position.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = argparser.parse_args(["--gpspos=35.6883 N, 139.7544 E", 
                                 "--gpsradius=20.0"])
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4623.jpg", "dsc_4664.jpg"]

def test_by_files(imgdir, argparser):
    """Select by file names.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = argparser.parse_args(["dsc_4664.jpg", "dsc_4831.jpg"])
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4664.jpg", "dsc_4831.jpg"]

def test_by_single_tag(imgdir, argparser):
    """Select by one single tag.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = argparser.parse_args(["--tags=Shinto_shrine"])
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4664.jpg", "dsc_4831.jpg"]

def test_by_mult_tags(imgdir, argparser):
    """Select by multiple tags.

    Combining multiple tags acts like an and, it selects only images
    having all the tags set.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = argparser.parse_args(["--tags=Tokyo,Shinto_shrine"])
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4664.jpg"]

def test_by_neg_tags(imgdir, argparser):
    """Select by negating tags.

    Prepending a tag by an exclamation mark selects the images having
    the tag not set.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = argparser.parse_args(["--tags=Tokyo,!Shinto_shrine"])
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4623.jpg"]

def test_by_empty_tag(imgdir, argparser):
    """Select by empty tags.

    The empty string as tag selects images having no tag.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = argparser.parse_args(["--tags="])
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_5126.jpg", "dsc_5167.jpg"]

def test_by_date_and_tag(imgdir, argparser):
    """Select by date and tags.

    Multiple selection criteria, such as date and tags may be
    combined.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = argparser.parse_args(["--tags=Tokyo", "--date=2016-02-28"])
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4623.jpg"]

def test_by_selected(imgdir, argparser):
    """Select by selected flag.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = argparser.parse_args(["--selected"])
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4664.jpg", "dsc_5126.jpg"]

def test_by_selected_and_tag(imgdir, argparser):
    """Select by selected flag and tag.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = argparser.parse_args(["--selected", "--tags=Tokyo"])
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4664.jpg"]

def test_by_not_selected(imgdir, argparser):
    """Select by not-selected flag.
    """
    idx = photo.index.Index(idxfile=imgdir)
    args = argparser.parse_args(["--not-selected"])
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == ["dsc_4623.jpg", "dsc_4831.jpg", "dsc_5167.jpg"]

