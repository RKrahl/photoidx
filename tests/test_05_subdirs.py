"""Images in subdirectories.

The Index class is supposed to provide limited support for the images
to be in subdirectories of the directory containing the index file.
All the tooling around does not use this feature for the time being,
though.
"""

import filecmp
import os
from pathlib import Path
import shutil
import subprocess
import pytest
import photoidx.index
import photoidx.idxfilter
from photoidx.geo import GeoPosition
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
        d = tmpdir / k
        d.mkdir()
        for f in testimgs[k]:
            shutil.copy(gettestdata(f), str(d / f))
    return tmpdir

@pytest.mark.dependency()
def test_create(imgdir):
    """Create the index.
    """
    with photoidx.index.Index(imgdir=imgdir) as idx:
        for k in ("Japan", "Quebec"):
            idx.extend_dir(imgdir / k)
        idx.write()
    idxfile = str(imgdir / ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"

@pytest.mark.dependency(depends=["test_create"])
def test_checksum(imgdir, monkeypatch):
    """Verify the checksum.

    As a side effect, this checks whether the image files are
    accessible by the filename stored in the index.
    """
    if not Path(checkprog).is_file():
        pytest.skip("%s not found." % checkprog)
    fname = imgdir / hashalg
    with photoidx.index.Index(idxfile=imgdir) as idx:
        with fname.open("wt") as f:
            for i in idx:
                print("%s  %s" % (i.checksum[hashalg], i.filename), file=f)
    monkeypatch.chdir(str(imgdir))
    with fname.open("rt") as f:
        cmd = [checkprog, "-c"]
        print(">", *cmd)
        subprocess.check_call(cmd, stdin=f)

@pytest.mark.dependency(depends=["test_create"])
def test_tag(imgdir, monkeypatch):
    """Test tagging of images.
    """
    with photoidx.index.Index(idxfile=imgdir) as idx:
        tokyo = GeoPosition("35.68 N, 139.77 E")
        idxfilter = photoidx.idxfilter.IdxFilter(gpspos=tokyo, gpsradius=500.0)
        for i in idxfilter.filter(idx):
            i.tags.add("Japan")
        quebec = GeoPosition("46.81 N, 71.22 W")
        idxfilter = photoidx.idxfilter.IdxFilter(gpspos=quebec, gpsradius=500.0)
        for i in idxfilter.filter(idx):
            i.tags.add("Quebec")
        idx.write()
    with photoidx.index.Index(idxfile=imgdir) as idx:
        for k in ("Japan", "Quebec"):
            idxfilter = photoidx.idxfilter.IdxFilter(tags=k)
            fnames = [ i.filename for i in idxfilter.filter(idx) ]
            assert fnames == [ Path(k, f) for f in testimgs[k] ]
