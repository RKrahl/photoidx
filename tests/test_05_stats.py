"""Get statistics about the items in an index from using class Stats.
"""

import datetime
import shutil
import pytest
import yaml
import photoidx.index
import photoidx.idxfilter
from photoidx.stats import Stats
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


def test_stats_all(imgdir):
    """Get statistics on all images.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        stats = Stats(idx)
    assert stats.count == 5
    assert stats.selected == 2
    assert stats.oldest == datetime.datetime(2016, 2, 28, 17, 26, 39)
    assert stats.newest == datetime.datetime(2016, 3, 9, 10, 7, 48)
    assert stats.by_date == {
        datetime.date(2016, 2, 28).toordinal() : 1,
        datetime.date(2016, 2, 29).toordinal() : 1,
        datetime.date(2016, 3, 5).toordinal() : 1,
        datetime.date(2016, 3, 8).toordinal() : 1,
        datetime.date(2016, 3, 9).toordinal() : 1,
    }
    assert stats.by_tag == {
        "Hakone": 1,
        "Shinto_shrine": 2,
        "Tokyo": 2,
    }

def test_stats_all_yaml(imgdir):
    """The string representation of a Stats object is YAML.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        stats = yaml.safe_load(str(Stats(idx)))
    assert stats["Count"] == 5
    assert stats["Selected"] == 2
    assert stats["Oldest"] == datetime.datetime(2016, 2, 28, 17, 26, 39)
    assert stats["Newest"] == datetime.datetime(2016, 3, 9, 10, 7, 48)
    assert stats["By date"] == {
        datetime.date(2016, 2, 28) : 1,
        datetime.date(2016, 2, 29) : 1,
        datetime.date(2016, 3, 5) : 1,
        datetime.date(2016, 3, 8) : 1,
        datetime.date(2016, 3, 9) : 1,
    }
    assert stats["By tag"] == {
        "Hakone": 1,
        "Shinto_shrine": 2,
        "Tokyo": 2,
    }

def test_stats_filtered(imgdir):
    """Get statistics on a selection of images.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        idxfilter = photoidx.idxfilter.IdxFilter(tags="Tokyo")
        stats = Stats(idxfilter.filter(idx))
    assert stats.count == 2
    assert stats.selected == 1
    assert stats.oldest == datetime.datetime(2016, 2, 28, 17, 26, 39)
    assert stats.newest == datetime.datetime(2016, 2, 29, 11, 37, 51)
    assert stats.by_date == {
        datetime.date(2016, 2, 28).toordinal() : 1,
        datetime.date(2016, 2, 29).toordinal() : 1,
    }
    assert stats.by_tag == {
        "Shinto_shrine": 1,
        "Tokyo": 2,
    }

