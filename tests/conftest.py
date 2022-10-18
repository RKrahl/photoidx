"""pytest configuration.
"""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import pytest
import photoidx


testdir = Path(__file__).parent

def gettestdata(fname):
    fname = testdir / "data" / fname
    assert fname.is_file()
    return str(fname)

@pytest.fixture(scope="module")
def tmpdir(request):
    td = tempfile.mkdtemp(prefix="photoidx-test-")
    yield Path(td)
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

def pytest_report_header(config):
    """Add information on the package version used in the tests.
    """
    modpath = Path(photoidx.__file__).resolve().parent
    return [ "photoidx: %s" % (photoidx.__version__),
             "          %s" % (modpath) ]
