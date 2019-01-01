"""pytest configuration.
"""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import pytest


testdir = Path(__file__).parent

def gettestdata(fname):
    fname = testdir.joinpath("data", fname)
    assert fname.is_file()
    return str(fname)

class TmpDir(object):
    """Provide a temporary directory.
    """
    def __init__(self):
        self.dir = Path(tempfile.mkdtemp(prefix="photo-test-"))
    def __del__(self):
        self.cleanup()
    def cleanup(self):
        if self.dir:
            shutil.rmtree(str(self.dir))
        self.dir = None

@pytest.fixture(scope="module")
def tmpdir(request):
    td = TmpDir()
    request.addfinalizer(td.cleanup)
    return td.dir

def callscript(scriptname, args, stdin=None, stdout=None, stderr=None):
    try:
        script_dir = os.environ['BUILD_SCRIPTS_DIR']
    except KeyError:
        pytest.skip("BUILD_SCRIPTS_DIR is not set.")
    script = Path(script_dir, scriptname)
    cmd = [sys.executable, str(script)] + args
    print("\n>", *cmd)
    subprocess.check_call(cmd, stdin=stdin, stdout=stdout, stderr=stderr)
