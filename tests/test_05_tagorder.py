"""Ordering of tags in the index file.  (Issue #9)

The tags are internally represented as a set, so they are not ordered.
This is correct, as it reflect the nature of tags.  In the index file,
they are represented as a list.  It would be desirable not to have
spurious differences in index files, e.g. two index files should be
equal unless there is a significant difference in the content.  That
is why the tags should have a well defined order in the index file.
"""

import filecmp
import shutil
import pytest
import photoidx.index
import photoidx.idxfilter
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
    return tmpdir

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

@pytest.mark.dependency()
def test_tag_ref(imgdir):
    idxfname = str(imgdir / ".index.yaml")
    reffname = str(imgdir / "index-ref.yaml")
    shutil.copy(gettestdata("index-create.yaml"), idxfname)
    with photoidx.index.Index(idxfile=imgdir) as idx:
        taglist = [ "Japan", "Tokyo", "Hakone", "Kyoto", 
                    "Ginza", "Shinto_shrine", "Geisha", "Ryoan-ji" ]
        for t in taglist:
            idxfilter = photoidx.idxfilter.IdxFilter(files=tags[t])
            for i in idxfilter.filter(idx):
                i.tags.add(t)
        idx.write()
    shutil.copy(idxfname, reffname)

@pytest.mark.dependency(depends=["test_tag_ref"])
def test_tag_shuffle(imgdir):
    """Same as test_tag_ref(), only the order of setting the tags differ.
    """
    idxfname = str(imgdir / ".index.yaml")
    reffname = str(imgdir / "index-ref.yaml")
    shutil.copy(gettestdata("index-create.yaml"), idxfname)
    with photoidx.index.Index(idxfile=imgdir) as idx:
        taglist = [ "Ginza", "Hakone", "Japan", "Geisha", 
                    "Shinto_shrine", "Tokyo", "Kyoto", "Ryoan-ji" ]
        for t in taglist:
            idxfilter = photoidx.idxfilter.IdxFilter(files=tags[t])
            for i in idxfilter.filter(idx):
                i.tags.add(t)
        idx.write()
    assert filecmp.cmp(idxfname, reffname), "index file differs from reference"

@pytest.mark.dependency(depends=["test_tag_ref"])
def test_tag_remove(imgdir):
    """First set all tags on all images, then remove the wrong ones.
    """
    idxfname = str(imgdir / ".index.yaml")
    reffname = str(imgdir / "index-ref.yaml")
    shutil.copy(gettestdata("index-create.yaml"), idxfname)
    with photoidx.index.Index(idxfile=imgdir) as idx:
        taglist = [ "Tokyo", "Shinto_shrine", "Ginza", "Geisha", 
                    "Japan", "Ryoan-ji", "Hakone", "Kyoto" ]
        for t in taglist:
            for i in idx:
                i.tags.add(t)
        for t in taglist:
            for i in idx:
                if str(i.filename) not in tags[t]:
                    i.tags.remove(t)
        idx.write()
    assert filecmp.cmp(idxfname, reffname), "index file differs from reference"

@pytest.mark.dependency(depends=["test_tag_ref"])
def test_tag_extra(imgdir):
    """Add a spurious extra tag first and remove it later.
    """
    idxfname = str(imgdir / ".index.yaml")
    reffname = str(imgdir / "index-ref.yaml")
    shutil.copy(gettestdata("index-create.yaml"), idxfname)
    with photoidx.index.Index(idxfile=imgdir) as idx:
        taglist = [ "Japan", "Tokyo", "Hakone", "Kyoto", 
                    "Ginza", "Shinto_shrine", "Geisha", "Ryoan-ji" ]
        for i in idx:
            i.tags.add("extra")
        for t in taglist:
            idxfilter = photoidx.idxfilter.IdxFilter(files=tags[t])
            for i in idxfilter.filter(idx):
                i.tags.add(t)
        for i in idx:
            i.tags.remove("extra")
        idx.write()
    assert filecmp.cmp(idxfname, reffname), "index file differs from reference"
