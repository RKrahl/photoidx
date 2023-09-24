"""Test different options to filter images by date.
"""

import datetime
import pytest
import photoidx.index
import photoidx.idxfilter
from conftest import gettestdata

testimgs = [ "dsc_%04d.jpg" % i for i in range(1,13) ]
indexfile = gettestdata("index-date.yaml")


def test_single_date():
    """Select by single date.
    """
    with photoidx.index.Index(idxfile=indexfile) as idx:
        date = (datetime.datetime(2016, 2, 29), datetime.datetime(2016, 3, 1))
        idxfilter = photoidx.idxfilter.IdxFilter(date=date)
        fnames = [ str(i.filename) for i in idxfilter.filter(idx) ]
        assert fnames == testimgs[1:4]


def test_interval_date_date():
    """Select by an interval between two dates.
    """
    with photoidx.index.Index(idxfile=indexfile) as idx:
        date = (datetime.datetime(2016, 2, 29), datetime.datetime(2016, 3, 6))
        idxfilter = photoidx.idxfilter.IdxFilter(date=date)
        fnames = [ str(i.filename) for i in idxfilter.filter(idx) ]
        assert fnames == testimgs[1:11]


def test_interval_date_datetime():
    """Select by an interval between start date and end date/time.
    """
    with photoidx.index.Index(idxfile=indexfile) as idx:
        date = (datetime.datetime(2016, 2, 29), 
                datetime.datetime(2016, 3, 5, 3, 47, 9))
        idxfilter = photoidx.idxfilter.IdxFilter(date=date)
        fnames = [ str(i.filename) for i in idxfilter.filter(idx) ]
        assert fnames == testimgs[1:9]


def test_single_datetime():
    """Select by single date/time.

    Probably not very useful in the praxis, but valid.
    """
    with photoidx.index.Index(idxfile=indexfile) as idx:
        date = (datetime.datetime(2016, 3, 3, 11, 21, 40), 
                datetime.datetime(2016, 3, 3, 11, 21, 41))
        idxfilter = photoidx.idxfilter.IdxFilter(date=date)
        fnames = [ str(i.filename) for i in idxfilter.filter(idx) ]
        assert fnames == testimgs[6:7]


def test_interval_datetime_date():
    """Select by an interval between start date/time and end date.
    """
    with photoidx.index.Index(idxfile=indexfile) as idx:
        date = (datetime.datetime(2016, 3, 3, 11, 21, 40), 
                datetime.datetime(2016, 3, 6))
        idxfilter = photoidx.idxfilter.IdxFilter(date=date)
        fnames = [ str(i.filename) for i in idxfilter.filter(idx) ]
        assert fnames == testimgs[6:11]


def test_interval_datetime_datetime():
    """Select by an interval between two date/times.
    """
    with photoidx.index.Index(idxfile=indexfile) as idx:
        date = (datetime.datetime(2016, 3, 3, 11, 21, 41), 
                datetime.datetime(2016, 3, 5, 3, 47, 9))
        idxfilter = photoidx.idxfilter.IdxFilter(date=date)
        fnames = [ str(i.filename) for i in idxfilter.filter(idx) ]
        assert fnames == testimgs[7:9]
