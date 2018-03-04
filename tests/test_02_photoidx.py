"""Call the command line script photoidx.py.
"""

from __future__ import print_function
import os.path
import shutil
import filecmp
import subprocess
import pytest
from conftest import tmpdir, gettestdata, callscript

testimgs = [ 
    "dsc_4623.jpg", "dsc_4664.jpg", "dsc_4831.jpg", 
    "dsc_5126.jpg", "dsc_5167.jpg" 
]
testimgfiles = [ gettestdata(i) for i in testimgs ]

refindex = gettestdata("index-create.yaml")

@pytest.fixture(scope="module")
def imgdir(tmpdir):
    for fname in testimgfiles:
        shutil.copy(fname, tmpdir)
    return tmpdir


# Note: the default value for the "-d" option to photoidx is the
# current working directory.  So changing to imgdir before calling
# photoidx without the "-d" option should be equivalent to calling
# "photoidx -d imgdir".  We more or less try both variants at random
# in the tests.

@pytest.mark.dependency()
def test_create(imgdir, monkeypatch):
    """Create the index.
    """
    monkeypatch.chdir(imgdir)
    callscript("photoidx.py", ["create"])
    idxfile = os.path.join(imgdir, ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"

@pytest.mark.dependency(depends=["test_create"])
def test_ls_all(imgdir):
    """List all images.
    """
    fname = os.path.join(imgdir, "out")
    with open(fname, "wt") as f:
        callscript("photoidx.py", ["-d", imgdir, "ls"], stdout=f)
    with open(fname, "rt") as f:
        out = f.read().split()
    assert out == testimgs

@pytest.mark.dependency(depends=["test_create"])
def test_ls_md5(imgdir, monkeypatch):
    """List with --checksum=md5 option.
    """
    md5sum = "/usr/bin/md5sum"
    if not os.path.isfile(md5sum):
        pytest.skip("md5sum not found.")
    monkeypatch.chdir(imgdir)
    fname = os.path.join(imgdir, "md5")
    with open(fname, "wt") as f:
        callscript("photoidx.py", ["ls", "--checksum=md5"], stdout=f)
    with open(fname, "rt") as f:
        cmd = [md5sum, "-c"]
        print(">", *cmd)
        subprocess.check_call(cmd, stdin=f)

@pytest.mark.dependency(depends=["test_create"])
def test_addtag_all(imgdir):
    """Tag all images.
    """
    args = ["-d", imgdir, "addtag", "all"]
    callscript("photoidx.py", args)
    fname = os.path.join(imgdir, "out")
    with open(fname, "wt") as f:
        args = ["-d", imgdir, "ls", "--tags", "all"]
        callscript("photoidx.py", args, stdout=f)
    with open(fname, "rt") as f:
        out = f.read().split()
    assert out == testimgs

@pytest.mark.dependency(depends=["test_create"])
def test_addtag_by_date(imgdir):
    """Select by date.
    """
    args = ["-d", imgdir, "addtag", "--date", "2016-03-05", "Hakone"]
    callscript("photoidx.py", args)
    fname = os.path.join(imgdir, "out")
    with open(fname, "wt") as f:
        args = ["-d", imgdir, "ls", "--tags", "Hakone"]
        callscript("photoidx.py", args, stdout=f)
    with open(fname, "rt") as f:
        out = f.read().split()
    assert out == ["dsc_4831.jpg"]

@pytest.mark.dependency(depends=["test_create"])
def test_addtag_by_gpspos(imgdir, monkeypatch):
    """Select by GPS position.
    """
    monkeypatch.chdir(imgdir)
    args = ["addtag", "--gpspos", "35.6883 N, 139.7544 E", 
            "--gpsradius", "20.0", "Tokyo"]
    callscript("photoidx.py", args)
    fname = os.path.join(imgdir, "out")
    with open(fname, "wt") as f:
        args = ["ls", "--tags", "Tokyo"]
        callscript("photoidx.py", args, stdout=f)
    with open(fname, "rt") as f:
        out = f.read().split()
    assert out == ["dsc_4623.jpg", "dsc_4664.jpg"]

@pytest.mark.dependency(depends=["test_create"])
def test_addtag_by_files(imgdir, monkeypatch):
    """Select by file names.
    """
    monkeypatch.chdir(imgdir)
    args = ["addtag", "Shinto_shrine", "dsc_4664.jpg", "dsc_4831.jpg"]
    callscript("photoidx.py", args)
    fname = os.path.join(imgdir, "out")
    with open(fname, "wt") as f:
        args = ["ls", "--tags", "Shinto_shrine"]
        callscript("photoidx.py", args, stdout=f)
    with open(fname, "rt") as f:
        out = f.read().split()
    assert out == ["dsc_4664.jpg", "dsc_4831.jpg"]

@pytest.mark.dependency(
    depends=["test_create", "test_addtag_all", "test_addtag_by_date", 
             "test_addtag_by_gpspos"]
)
def test_rmtag_by_tag(imgdir, monkeypatch):
    """Remove a tag from images selected by tags.
    """
    monkeypatch.chdir(imgdir)
    args = ["rmtag", "--tags", "Tokyo", "all"]
    callscript("photoidx.py", args)
    args = ["rmtag", "--tags", "Hakone", "all"]
    callscript("photoidx.py", args)
    fname = os.path.join(imgdir, "out")
    with open(fname, "wt") as f:
        args = ["ls", "--tags", "all"]
        callscript("photoidx.py", args, stdout=f)
    with open(fname, "rt") as f:
        out = f.read().split()
    assert out == ["dsc_5126.jpg", "dsc_5167.jpg"]

@pytest.mark.dependency(depends=["test_create", "test_addtag_all"])
def test_rmtag_all(imgdir, monkeypatch):
    """Remove a tag from all images.
    """
    monkeypatch.chdir(imgdir)
    args = ["-d", imgdir, "rmtag", "all"]
    callscript("photoidx.py", args)
    fname = os.path.join(imgdir, "out")
    with open(fname, "wt") as f:
        args = ["-d", imgdir, "ls", "--tags", "all"]
        callscript("photoidx.py", args, stdout=f)
    with open(fname, "rt") as f:
        out = f.read().split()
    assert out == []

@pytest.mark.dependency(depends=["test_create", "test_addtag_by_files"])
def test_ls_by_single_tag(imgdir):
    """Select by one single tag.
    """
    fname = os.path.join(imgdir, "out")
    with open(fname, "wt") as f:
        args = ["-d", imgdir, "ls", "--tags", "Shinto_shrine"]
        callscript("photoidx.py", args, stdout=f)
    with open(fname, "rt") as f:
        out = f.read().split()
    assert out == ["dsc_4664.jpg", "dsc_4831.jpg"]

@pytest.mark.dependency(
    depends=["test_create", "test_addtag_by_gpspos", "test_addtag_by_files"]
)
def test_ls_by_mult_tags(imgdir):
    """Select by multiple tags.

    Combining multiple tags acts like an and, it selects only images
    having all the tags set.
    """
    fname = os.path.join(imgdir, "out")
    with open(fname, "wt") as f:
        args = ["-d", imgdir, "ls", "--tags", "Tokyo,Shinto_shrine"]
        callscript("photoidx.py", args, stdout=f)
    with open(fname, "rt") as f:
        out = f.read().split()
    assert out == ["dsc_4664.jpg"]

@pytest.mark.dependency(
    depends=["test_create", "test_addtag_by_gpspos", "test_addtag_by_files"]
)
def test_ls_by_neg_tags(imgdir, monkeypatch):
    """Select by negating tags.

    Prepending a tag by an exclamation mark selects the images having
    the tag not set.
    """
    monkeypatch.chdir(imgdir)
    fname = os.path.join(imgdir, "out")
    with open(fname, "wt") as f:
        args = ["ls", "--tags", "Tokyo,!Shinto_shrine"]
        callscript("photoidx.py", args, stdout=f)
    with open(fname, "rt") as f:
        out = f.read().split()
    assert out == ["dsc_4623.jpg"]

@pytest.mark.dependency(
    depends=["test_create", "test_addtag_by_date", "test_addtag_by_gpspos", 
             "test_addtag_by_files"]
)
def test_ls_by_empty_tag(imgdir):
    """Select by empty tags.

    The option tags with empty value selects images having no tag.
    """
    fname = os.path.join(imgdir, "out")
    with open(fname, "wt") as f:
        args = ["-d", imgdir, "ls", "--tags", ""]
        callscript("photoidx.py", args, stdout=f)
    with open(fname, "rt") as f:
        out = f.read().split()
    assert out == ["dsc_5126.jpg", "dsc_5167.jpg"]

@pytest.mark.dependency(depends=["test_create", "test_addtag_by_gpspos"])
def test_ls_by_date_and_tag(imgdir):
    """Select by date and tags.

    Multiple selection criteria, such as date and tags may be
    combined.
    """
    fname = os.path.join(imgdir, "out")
    with open(fname, "wt") as f:
        args = ["-d", imgdir, "ls", "--tags", "Tokyo", "--date", "2016-02-28"]
        callscript("photoidx.py", args, stdout=f)
    with open(fname, "rt") as f:
        out = f.read().split()
    assert out == ["dsc_4623.jpg"]

@pytest.mark.dependency(
    depends=["test_create", "test_addtag_by_date", "test_addtag_by_gpspos", 
             "test_addtag_by_files"]
)
def test_lstags_all(imgdir):
    """List tags.
    """
    fname = os.path.join(imgdir, "out")
    with open(fname, "wt") as f:
        args = ["-d", imgdir, "lstags"]
        callscript("photoidx.py", args, stdout=f)
    with open(fname, "rt") as f:
        out = f.read().split()
    assert out == ["Hakone", "Shinto_shrine", "Tokyo"]

@pytest.mark.dependency(
    depends=["test_create", "test_addtag_by_gpspos", "test_addtag_by_files"]
)
def test_lstags_by_tags(imgdir, monkeypatch):
    """List tags selected by tags.
    """
    monkeypatch.chdir(imgdir)
    fname = os.path.join(imgdir, "out")
    with open(fname, "wt") as f:
        args = ["lstags", "--tags", "Tokyo"]
        callscript("photoidx.py", args, stdout=f)
    with open(fname, "rt") as f:
        out = f.read().split()
    assert out == ["Shinto_shrine", "Tokyo"]

@pytest.mark.dependency(depends=["test_create"])
def test_select_by_files(imgdir, monkeypatch):
    """Select by file names.
    """
    monkeypatch.chdir(imgdir)
    args = ["select", "dsc_5126.jpg"]
    callscript("photoidx.py", args)
    fname = os.path.join(imgdir, "out")
    with open(fname, "wt") as f:
        args = ["ls", "--selected"]
        callscript("photoidx.py", args, stdout=f)
    with open(fname, "rt") as f:
        out = f.read().split()
    assert out == ["dsc_5126.jpg"]

@pytest.mark.dependency(
    depends=["test_create", "test_addtag_by_files", "test_select_by_files"]
)
def test_select_by_tag(imgdir, monkeypatch):
    """Select by tag.
    """
    monkeypatch.chdir(imgdir)
    args = ["select", "--tags", "Shinto_shrine"]
    callscript("photoidx.py", args)
    fname = os.path.join(imgdir, "out")
    with open(fname, "wt") as f:
        args = ["ls", "--selected"]
        callscript("photoidx.py", args, stdout=f)
    with open(fname, "rt") as f:
        out = f.read().split()
    assert out == ["dsc_4664.jpg", "dsc_4831.jpg", "dsc_5126.jpg"]

@pytest.mark.dependency(depends=["test_create", "test_select_by_tag"])
def test_deselect_by_files(imgdir, monkeypatch):
    """Deselect by file names.
    """
    monkeypatch.chdir(imgdir)
    args = ["deselect", "dsc_4831.jpg"]
    callscript("photoidx.py", args)
    fname = os.path.join(imgdir, "out")
    with open(fname, "wt") as f:
        args = ["ls", "--selected"]
        callscript("photoidx.py", args, stdout=f)
    with open(fname, "rt") as f:
        out = f.read().split()
    assert out == ["dsc_4664.jpg", "dsc_5126.jpg"]
