"""Images in subdirectories.

The Index class is supposed to provide limited support for the images
to be in subdirectories of the directory containing the index file.
All the tooling around does not use this feature for the time being,
though.
"""

import filecmp
import os
import os.path
import shutil
import subprocess
import pytest
import photo.index
import photo.idxfilter
from photo.geo import GeoPosition
from conftest import tmpdir, gettestdata

testimgs = {
    "Japan": [ "dsc_4623.jpg", "dsc_4664.jpg", "dsc_4831.jpg", "dsc_5167.jpg" ],
    "Quebec": [ "dsc_7157.jpg", "dsc_7490.jpg", "dsc_7582.jpg" ],
}
refindex = gettestdata("index-subdirs.yaml")

hashalg = "md5"
checkprog = "/usr/bin/md5sum"


@pytest.fixture(scope="module")
def imgdir(tmpdir):
    for k in testimgs.keys():
        d = os.path.join(tmpdir, k)
        os.mkdir(d)
        for f in testimgs[k]:
            shutil.copy(gettestdata(f), os.path.join(d, f))
    return tmpdir

@pytest.mark.dependency()
def test_create(imgdir):
    """Create the index.
    """
    idx = photo.index.Index(imgdir=imgdir)
    idx.write()
    for k in ("Japan", "Quebec"):
        idx = photo.index.Index(idxfile=imgdir, imgdir=os.path.join(imgdir, k))
        idx.write()
    idxfile = os.path.join(imgdir, ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"

@pytest.mark.dependency(depends=["test_create"])
def test_checksum(imgdir, monkeypatch):
    """Verify the checksum.

    As a side effect, this checks whether the image files are
    accessible by the filename stored in the index.
    """
    if not os.path.isfile(checkprog):
        pytest.skip("%s not found." % checkprog)
    fname = os.path.join(imgdir, hashalg)
    idx = photo.index.Index(idxfile=imgdir)
    with open(fname, "wt") as f:
        for i in idx:
            print("%s  %s" % (i.checksum[hashalg], i.filename), file=f)
    monkeypatch.chdir(imgdir)
    with open(fname, "rt") as f:
        cmd = [checkprog, "-c"]
        print(">", *cmd)
        subprocess.check_call(cmd, stdin=f)

@pytest.mark.dependency(depends=["test_create"])
def test_tag(imgdir, monkeypatch):
    """Test tagging of images.
    """
    idx = photo.index.Index(idxfile=imgdir)
    tokyo = GeoPosition("35.68 N, 139.77 E")
    idxfilter = photo.idxfilter.IdxFilter(gpspos=tokyo, gpsradius=500.0)
    for i in idxfilter.filter(idx):
        i.tags.add("Japan")
    quebec = GeoPosition("46.81 N, 71.22 W")
    idxfilter = photo.idxfilter.IdxFilter(gpspos=quebec, gpsradius=500.0)
    for i in idxfilter.filter(idx):
        i.tags.add("Quebec")
    idx.write()
    idx = photo.index.Index(idxfile=imgdir)
    for k in ("Japan", "Quebec"):
        idxfilter = photo.idxfilter.IdxFilter(tags=k)
        fnames = [ i.filename for i in idxfilter.filter(idx) ]
        assert fnames == [ os.path.join(k, f) for f in testimgs[k] ]
