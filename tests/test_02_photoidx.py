"""Call the command line script photo-idx.py.
"""

import datetime
import filecmp
from pathlib import Path
import shutil
import subprocess
import pytest
import yaml
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
        shutil.copy(fname, str(tmpdir))
    return tmpdir


# Note: the default value for the "-d" option to photo-idx is the
# current working directory.  So changing to imgdir before calling
# photo-idx without the "-d" option should be equivalent to calling
# "photo-idx -d imgdir".  We more or less try both variants at random
# in the tests.

@pytest.mark.dependency()
def test_create(imgdir, monkeypatch):
    """Create the index.
    """
    monkeypatch.chdir(str(imgdir))
    callscript("photo-idx.py", ["create"])
    idxfile = str(imgdir / ".index.yaml")
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"

@pytest.mark.dependency(depends=["test_create"])
def test_ls_all(imgdir):
    """List all images.
    """
    fname = imgdir / "out"
    with fname.open("wt") as f:
        callscript("photo-idx.py", ["-d", str(imgdir), "ls"], stdout=f)
    with fname.open("rt") as f:
        out = f.read().split()
    assert out == testimgs

@pytest.mark.dependency(depends=["test_create"])
def test_ls_md5(imgdir, monkeypatch):
    """List with --checksum=md5 option.
    """
    md5sum = "/usr/bin/md5sum"
    if not Path(md5sum).is_file():
        pytest.skip("md5sum not found.")
    monkeypatch.chdir(str(imgdir))
    fname = imgdir / "md5"
    with fname.open("wt") as f:
        callscript("photo-idx.py", ["ls", "--checksum=md5"], stdout=f)
    with fname.open("rt") as f:
        cmd = [md5sum, "-c"]
        print(">", *cmd)
        subprocess.check_call(cmd, stdin=f)

@pytest.mark.dependency(depends=["test_create"])
def test_addtag_all(imgdir):
    """Tag all images.
    """
    args = ["-d", str(imgdir), "addtag", "all"]
    callscript("photo-idx.py", args)
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["-d", str(imgdir), "ls", "--tags", "all"]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
        out = f.read().split()
    assert out == testimgs

@pytest.mark.dependency(depends=["test_create"])
def test_addtag_by_date(imgdir):
    """Select by date.
    """
    args = ["-d", str(imgdir), "addtag", "--date", "2016-03-05", "Hakone"]
    callscript("photo-idx.py", args)
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["-d", str(imgdir), "ls", "--tags", "Hakone"]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
        out = f.read().split()
    assert out == ["dsc_4831.jpg"]

@pytest.mark.dependency(depends=["test_create"])
def test_addtag_by_gpspos(imgdir, monkeypatch):
    """Select by GPS position.
    """
    monkeypatch.chdir(str(imgdir))
    args = ["addtag", "--gpspos", "35.6883 N, 139.7544 E", 
            "--gpsradius", "20.0", "Tokyo"]
    callscript("photo-idx.py", args)
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["ls", "--tags", "Tokyo"]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
        out = f.read().split()
    assert out == ["dsc_4623.jpg", "dsc_4664.jpg"]

@pytest.mark.dependency(depends=["test_create"])
def test_addtag_by_files(imgdir, monkeypatch):
    """Select by file names.
    """
    monkeypatch.chdir(str(imgdir))
    args = ["addtag", "Shinto_shrine", "dsc_4664.jpg", "dsc_4831.jpg"]
    callscript("photo-idx.py", args)
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["ls", "--tags", "Shinto_shrine"]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
        out = f.read().split()
    assert out == ["dsc_4664.jpg", "dsc_4831.jpg"]

@pytest.mark.dependency(
    depends=["test_create", "test_addtag_all", "test_addtag_by_date", 
             "test_addtag_by_gpspos"]
)
def test_rmtag_by_tag(imgdir, monkeypatch):
    """Remove a tag from images selected by tags.
    """
    monkeypatch.chdir(str(imgdir))
    args = ["rmtag", "--tags", "Tokyo", "all"]
    callscript("photo-idx.py", args)
    args = ["rmtag", "--tags", "Hakone", "all"]
    callscript("photo-idx.py", args)
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["ls", "--tags", "all"]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
        out = f.read().split()
    assert out == ["dsc_5126.jpg", "dsc_5167.jpg"]

@pytest.mark.dependency(depends=["test_create", "test_addtag_all"])
def test_rmtag_all(imgdir, monkeypatch):
    """Remove a tag from all images.
    """
    monkeypatch.chdir(str(imgdir))
    args = ["-d", str(imgdir), "rmtag", "all"]
    callscript("photo-idx.py", args)
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["-d", str(imgdir), "ls", "--tags", "all"]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
        out = f.read().split()
    assert out == []

@pytest.mark.dependency(depends=["test_create", "test_addtag_by_files"])
def test_ls_by_single_tag(imgdir):
    """Select by one single tag.
    """
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["-d", str(imgdir), "ls", "--tags", "Shinto_shrine"]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
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
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["-d", str(imgdir), "ls", "--tags", "Tokyo,Shinto_shrine"]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
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
    monkeypatch.chdir(str(imgdir))
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["ls", "--tags", "Tokyo,!Shinto_shrine"]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
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
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["-d", str(imgdir), "ls", "--tags", ""]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
        out = f.read().split()
    assert out == ["dsc_5126.jpg", "dsc_5167.jpg"]

@pytest.mark.dependency(depends=["test_create", "test_addtag_by_gpspos"])
def test_ls_by_date_and_tag(imgdir):
    """Select by date and tags.

    Multiple selection criteria, such as date and tags may be
    combined.
    """
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["-d", str(imgdir), "ls", 
                "--tags", "Tokyo", "--date", "2016-02-28"]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
        out = f.read().split()
    assert out == ["dsc_4623.jpg"]

@pytest.mark.dependency(
    depends=["test_create", "test_addtag_by_date", "test_addtag_by_gpspos", 
             "test_addtag_by_files"]
)
def test_lstags_all(imgdir):
    """List tags.
    """
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["-d", str(imgdir), "lstags"]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
        out = f.read().split()
    assert out == ["Hakone", "Shinto_shrine", "Tokyo"]

@pytest.mark.dependency(
    depends=["test_create", "test_addtag_by_gpspos", "test_addtag_by_files"]
)
def test_lstags_by_tags(imgdir, monkeypatch):
    """List tags selected by tags.
    """
    monkeypatch.chdir(str(imgdir))
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["lstags", "--tags", "Tokyo"]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
        out = f.read().split()
    assert out == ["Shinto_shrine", "Tokyo"]

@pytest.mark.dependency(depends=["test_create"])
def test_select_by_files(imgdir, monkeypatch):
    """Select by file names.
    """
    monkeypatch.chdir(str(imgdir))
    args = ["select", "dsc_5126.jpg"]
    callscript("photo-idx.py", args)
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["ls", "--selected"]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
        out = f.read().split()
    assert out == ["dsc_5126.jpg"]

@pytest.mark.dependency(
    depends=["test_create", "test_addtag_by_files", "test_select_by_files"]
)
def test_select_by_tag(imgdir, monkeypatch):
    """Select by tag.
    """
    monkeypatch.chdir(str(imgdir))
    args = ["select", "--tags", "Shinto_shrine"]
    callscript("photo-idx.py", args)
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["ls", "--selected"]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
        out = f.read().split()
    assert out == ["dsc_4664.jpg", "dsc_4831.jpg", "dsc_5126.jpg"]

@pytest.mark.dependency(depends=["test_create", "test_select_by_tag"])
def test_deselect_by_files(imgdir, monkeypatch):
    """Deselect by file names.
    """
    monkeypatch.chdir(str(imgdir))
    args = ["deselect", "dsc_4831.jpg"]
    callscript("photo-idx.py", args)
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["ls", "--selected"]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
        out = f.read().split()
    assert out == ["dsc_4664.jpg", "dsc_5126.jpg"]

@pytest.mark.dependency(
    depends=["test_create", "test_addtag_by_date", "test_addtag_by_gpspos", 
             "test_addtag_by_files", "test_rmtag_all"]
)
def test_stats_all(imgdir):
    """Show stats.
    """
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["-d", str(imgdir), "stats"]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
        stats = yaml.safe_load(f)
    assert stats["Count"] == 5
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

@pytest.mark.dependency(
    depends=["test_create", "test_addtag_by_date", "test_addtag_by_gpspos", 
             "test_addtag_by_files", "test_rmtag_all"]
)
def test_stats_filtered(imgdir):
    """Show stats on a selection.
    """
    fname = imgdir / "out"
    with fname.open("wt") as f:
        args = ["-d", str(imgdir), "stats", "--tags", "Tokyo"]
        callscript("photo-idx.py", args, stdout=f)
    with fname.open("rt") as f:
        stats = yaml.safe_load(f)
    assert stats["Count"] == 2
    assert stats["Oldest"] == datetime.datetime(2016, 2, 28, 17, 26, 39)
    assert stats["Newest"] == datetime.datetime(2016, 2, 29, 11, 37, 51)
    assert stats["By date"] == {
        datetime.date(2016, 2, 28) : 1,
        datetime.date(2016, 2, 29) : 1,
    }
    assert stats["By tag"] == {
        "Shinto_shrine": 1,
        "Tokyo": 2,
    }
