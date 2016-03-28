"""Ordering of tags in the index file.  (Issue #9)

The tags are internally represented as a set, so they are not ordered.
This is correct, as it reflect the nature of tags.  In the index file,
they are represented as a list.  It would be desirable not to have
spurious differences in index files, e.g. two index files should be
equal unless there is a significant difference in the content.  That
is why the tags should have a well defined order in the index file.
"""

import os.path
import shutil
import filecmp
import pytest
import photo.index
import photo.idxfilter
from conftest import tmpdir, gettestdata, testimgs


@pytest.fixture(scope="module")
def imgdir(tmpdir):
    for fname in testimgs:
        shutil.copy(gettestdata(fname), tmpdir)
    return tmpdir

class NameSpace(object):
    def __init__(self, **kwargs):
        for k in ["tags", "date", "gpspos", "gpsradius", "files"]:
            setattr(self, k, None)
        for k in kwargs:
            setattr(self, k, kwargs[k])

# Each test ends up adding the same set of tags to each image.  But
# the order in which the tags are added differs between tests and some
# test also adds spurious tags and removes them later.  The list order
# of elements in a set depends on the history of insertions and
# deletions.  The resulting index file should not be affected by this
# and should always have the same order.  Before fixing Issue #9, the
# arbitrary list order of the set was also in the index file.

tags = {
    "Japan": testimgs,
    "Tokyo": ["dsc_4623.jpg", "dsc_4664.jpg"],
    "Hakone": ["dsc_4831.jpg"],
    "Kyoto": ["dsc_5126.jpg", "dsc_5167.jpg"],
    "Ginza": ["dsc_4623.jpg"],
    "Shinto_shrine": ["dsc_4664.jpg", "dsc_4831.jpg"],
    "Geisha": ["dsc_5126.jpg"],
    "Ryoan-ji": ["dsc_5167.jpg"],
}

def test_tag_ref(imgdir):
    idxfname = os.path.join(imgdir, ".index.yaml")
    reffname = os.path.join(imgdir, "index-ref.yaml")
    shutil.copy(gettestdata("index-create.yaml"), idxfname)
    idx = photo.index.Index(idxfile=imgdir)
    taglist = [ "Japan", "Tokyo", "Hakone", "Kyoto", 
                "Ginza", "Shinto_shrine", "Geisha", "Ryoan-ji" ]
    for t in taglist:
        args = NameSpace(files=tags[t])
        idxfilter = photo.idxfilter.IdxFilter(args)
        for i in filter(idxfilter, idx):
            i.tags.add(t)
    idx.write()
    shutil.copy(idxfname, reffname)

def test_tag_shuffle(imgdir):
    """Same as test_tag_ref(), only the order of setting the tags differ.
    """
    idxfname = os.path.join(imgdir, ".index.yaml")
    reffname = os.path.join(imgdir, "index-ref.yaml")
    shutil.copy(gettestdata("index-create.yaml"), idxfname)
    idx = photo.index.Index(idxfile=imgdir)
    taglist = [ "Ginza", "Hakone", "Japan", "Geisha", 
                "Shinto_shrine", "Tokyo", "Kyoto", "Ryoan-ji" ]
    for t in taglist:
        args = NameSpace(files=tags[t])
        idxfilter = photo.idxfilter.IdxFilter(args)
        for i in filter(idxfilter, idx):
            i.tags.add(t)
    idx.write()
    assert filecmp.cmp(idxfname, reffname), "index file differs from reference"

def test_tag_remove(imgdir):
    """First set all tags on all images, then remove the wrong ones.
    """
    idxfname = os.path.join(imgdir, ".index.yaml")
    reffname = os.path.join(imgdir, "index-ref.yaml")
    shutil.copy(gettestdata("index-create.yaml"), idxfname)
    idx = photo.index.Index(idxfile=imgdir)
    taglist = [ "Tokyo", "Shinto_shrine", "Ginza", "Geisha", 
                "Japan", "Ryoan-ji", "Hakone", "Kyoto" ]
    for t in taglist:
        for i in idx:
            i.tags.add(t)
    for t in taglist:
        for i in idx:
            if i.filename not in tags[t]:
                i.tags.remove(t)
    idx.write()
    assert filecmp.cmp(idxfname, reffname), "index file differs from reference"

def test_tag_extra(imgdir):
    """Add a spurious extra tag first and remove it later.
    """
    idxfname = os.path.join(imgdir, ".index.yaml")
    reffname = os.path.join(imgdir, "index-ref.yaml")
    shutil.copy(gettestdata("index-create.yaml"), idxfname)
    idx = photo.index.Index(idxfile=imgdir)
    taglist = [ "Japan", "Tokyo", "Hakone", "Kyoto", 
                "Ginza", "Shinto_shrine", "Geisha", "Ryoan-ji" ]
    for i in idx:
        i.tags.add("extra")
    for t in taglist:
        args = NameSpace(files=tags[t])
        idxfilter = photo.idxfilter.IdxFilter(args)
        for i in filter(idxfilter, idx):
            i.tags.add(t)
    for i in idx:
        i.tags.remove("extra")
    idx.write()
    assert filecmp.cmp(idxfname, reffname), "index file differs from reference"
