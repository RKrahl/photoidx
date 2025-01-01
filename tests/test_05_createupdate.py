"""Add images to an index.
"""

import shutil
import pytest
from photoidx.datetools import gettz
import photoidx.index
from conftest import tmpdir, gettestdata, index_cmp

testimgs = [ 
    "dsc_4623.jpg", "dsc_4664.jpg", "dsc_4831.jpg", 
    "dsc_5126.jpg", "dsc_5167.jpg" 
]
testimgfiles = [ gettestdata(i) for i in testimgs ]

refindex = gettestdata("index.yaml")

def test_createupdate(tmpdir):
    """Create an index and then update it, adding a few more images.
    """
    workdir = tmpdir / "t1"
    workdir.mkdir()
    for fname in testimgfiles[:2]:
        shutil.copy(fname, workdir)
    with photoidx.index.Index(imgdir=workdir,
                              comment="Japan 2016",
                              default_tz=gettz("Asia/Tokyo")) as idx:
        idx.write()
        assert idx.head['TimeZone'] == "Asia/Tokyo"
    for fname in testimgfiles[2:]:
        shutil.copy(fname, workdir)
    with photoidx.index.Index(idxfile=workdir, imgdir=workdir) as idx:
        idx.write()
        assert idx.head['TimeZone'] == "Asia/Tokyo"
    idxfile = workdir / ".index.yaml"
    assert index_cmp(idxfile, refindex), "index file differs from reference"

def test_createupdate_change_comment(tmpdir):
    """Same as last test, but also change the comment in the update.
    """
    workdir = tmpdir / "t2"
    workdir.mkdir()
    for fname in testimgfiles[:2]:
        shutil.copy(fname, workdir)
    with photoidx.index.Index(imgdir=workdir,
                              comment="Japan 2016 first round",
                              default_tz=gettz()) as idx:
        idx.write()
        assert idx.head['TimeZone'] == "Europe/Berlin"
    for fname in testimgfiles[2:]:
        shutil.copy(fname, workdir)
    with photoidx.index.Index(idxfile=workdir, imgdir=workdir,
                              comment="Japan 2016",
                              default_tz=gettz("Asia/Tokyo")) as idx:
        idx.write()
        assert idx.head['TimeZone'] == "Asia/Tokyo"
    idxfile = workdir / ".index.yaml"
    assert index_cmp(idxfile, refindex), "index file differs from reference"
