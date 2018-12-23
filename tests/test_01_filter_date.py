"""Test different options to filter images by date.
"""

import pytest
import photo.index
import photo.idxfilter
from conftest import gettestdata

testimgs = [ "dsc_%04d.jpg" % i for i in range(1,13) ]
indexfile = gettestdata("index-date.yaml")


def test_single_date():
    """Select by single date.
    """
    idx = photo.index.Index(idxfile=indexfile)
    idxfilter = photo.idxfilter.IdxFilter(date="2016-02-29")
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == testimgs[1:4]


def test_interval_date_date():
    """Select by an interval between two dates.
    """
    idx = photo.index.Index(idxfile=indexfile)
    idxfilter = photo.idxfilter.IdxFilter(date="2016-02-29--2016-03-05")
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == testimgs[1:11]


def test_interval_date_datetime():
    """Select by an interval between start date and end date/time.
    """
    idx = photo.index.Index(idxfile=indexfile)
    idxfilter = photo.idxfilter.IdxFilter(date="2016-02-29/2016-03-05T03:47:08")
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == testimgs[1:9]


def test_single_datetime():
    """Select by single date/time.

    Probably not very useful in the praxis, but valid.
    """
    idx = photo.index.Index(idxfile=indexfile)
    idxfilter = photo.idxfilter.IdxFilter(date="2016-03-03T11:21:40")
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == testimgs[6:7]


def test_interval_datetime_date():
    """Select by an interval between start date/time and end date.
    """
    idx = photo.index.Index(idxfile=indexfile)
    idxfilter = photo.idxfilter.IdxFilter(date="2016-03-03T11:21:40/2016-03-05")
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == testimgs[6:11]


def test_interval_datetime_datetime():
    """Select by an interval between two date/times.
    """
    idx = photo.index.Index(idxfile=indexfile)
    idxfilter = photo.idxfilter.IdxFilter(
        date="2016-03-03T11:21:41--2016-03-05T03:47:08"
    )
    fnames = [ i.filename for i in idxfilter.filter(idx) ]
    assert fnames == testimgs[7:9]
