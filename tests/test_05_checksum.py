"""Check checksums.
"""

from pathlib import Path
import shutil
import subprocess
import pytest
import photoidx.index
from conftest import tmpdir, gettestdata

testimgs = [ 
    "dsc_4623.jpg", "dsc_4664.jpg", "dsc_4831.jpg", 
    "dsc_5126.jpg", "dsc_5167.jpg" 
]
testimgfiles = [ gettestdata(i) for i in testimgs ]

hashalg = {
    "md5": "/usr/bin/md5sum",
    "sha1": "/usr/bin/sha1sum",
    "sha224": "/usr/bin/sha224sum",
    "sha256": "/usr/bin/sha256sum",
    "sha384": "/usr/bin/sha384sum",
    "sha512": "/usr/bin/sha512sum",
}

@pytest.mark.dependency()
def test_create_checksum(tmpdir):
    for fname in testimgfiles:
        shutil.copy(fname, str(tmpdir))
    with photoidx.index.Index(imgdir=tmpdir, hashalg=hashalg.keys()) as idx:
        idx.write()

@pytest.mark.dependency(depends=["test_create_checksum"])
@pytest.mark.parametrize("alg", hashalg.keys())
def test_check_checksum(tmpdir, monkeypatch, alg):
    checkprog = hashalg[alg]
    if not Path(checkprog).is_file():
        pytest.skip("%s not found." % checkprog)
    fname = tmpdir / alg
    with photoidx.index.Index(idxfile=tmpdir) as idx, fname.open("wt") as f:
        for i in idx:
            print("%s  %s" % (i.checksum[alg], i.filename), file=f)
    monkeypatch.chdir(str(tmpdir))
    with fname.open("rt") as f:
        cmd = [checkprog, "-c"]
        print(">", *cmd)
        subprocess.check_call(cmd, stdin=f)

def test_no_checksum(tmpdir):
    with photoidx.index.Index(imgdir=tmpdir, hashalg=[]) as idx:
        idx.write()
    with photoidx.index.Index(idxfile=tmpdir) as idx:
        for i in idx:
            assert i.checksum == {}
