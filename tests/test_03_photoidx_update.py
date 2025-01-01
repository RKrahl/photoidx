"""Call the update subcommand in command line script photo-idx.py.
"""

import datetime
from pathlib import Path
import shutil
import subprocess
import pytest
import yaml
from conftest import tmpdir, gettestdata, callscript, index_cmp

testimgs = [ 
    "dsc_4623.jpg", "dsc_4664.jpg", "dsc_4831.jpg", 
    "dsc_5126.jpg", "dsc_5167.jpg" 
]
testimgfiles = [ gettestdata(i) for i in testimgs ]
refindex = gettestdata("index-md5-sha1.yaml")


def test_createupdate(tmpdir):
    """Create an index and then update it, adding a few more images.
    """
    for fname in testimgfiles[:2]:
        shutil.copy(fname, tmpdir)
    callscript("photo-idx.py", ["-d", str(tmpdir), "create",
                                "--comment", "Japan 2016 first round",
                                "--checksums", "md5,sha1"])
    for fname in testimgfiles[2:]:
        shutil.copy(fname, tmpdir)
    callscript("photo-idx.py", ["-d", str(tmpdir), "update",
                                "--comment", "Japan 2016",
                                "--timezone", "Asia/Tokyo"])
    idxfile = tmpdir / ".index.yaml"
    assert index_cmp(idxfile, refindex), "index file differs from reference"
