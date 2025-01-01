"""pytest configuration.
"""

import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import pytest
import photoidx


testdir = Path(__file__).parent

# Some tests might need to make assumptions on the local time zone.
# So define that boundary condition right from the beginning.
os.environ["TZ"] = "Europe/Berlin"
time.tzset()

def gettestdata(fname):
    fname = testdir / "data" / fname
    assert fname.is_file()
    return fname

@pytest.fixture(scope="module")
def tmpdir(request):
    td = Path(tempfile.mkdtemp(prefix="photoidx-test-"))
    yield td
    shutil.rmtree(td)

def callscript(scriptname, args, stdin=None, stdout=None, stderr=None):
    try:
        script_dir = os.environ['BUILD_SCRIPTS_DIR']
    except KeyError:
        pytest.skip("BUILD_SCRIPTS_DIR is not set.")
    script = Path(script_dir, scriptname)
    cmd = [sys.executable, str(script)] + args
    print("\n>", *cmd)
    subprocess.check_call(cmd, stdin=stdin, stdout=stdout, stderr=stderr)

_idx_cmp_ignore_re = re.compile(r"^Date:\s")

def index_cmp(p1, p2):
    """Compare two index files, ignoring the 'Date:' line in the header.
    """
    with p1.open("rt") as f1, p2.open("rt") as f2:
        while True:
            l1 = f1.readline()
            l2 = f2.readline()
            if not(l1) and not(l2):
                return True
            if _idx_cmp_ignore_re.match(l1) and _idx_cmp_ignore_re.match(l2):
                continue
            if l1 != l2:
                return False

def pytest_report_header(config):
    """Add information on the package version used in the tests.
    """
    modpath = Path(photoidx.__file__).resolve().parent
    return [ "photoidx: %s" % (photoidx.__version__),
             "          %s" % (modpath) ]
