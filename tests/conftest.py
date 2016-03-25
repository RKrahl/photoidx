"""pytest configuration.
"""

import os.path
import tempfile
import shutil
import pytest


testdir = os.path.dirname(__file__)

def gettestdata(fname):
    fname = os.path.join(testdir, "data", fname)
    assert os.path.isfile(fname)
    return fname

class TmpDir(object):
    """Provide a temporary directory.
    """
    def __init__(self):
        self.dir = tempfile.mkdtemp(prefix="photo-test-")
    def __del__(self):
        self.cleanup()
    def cleanup(self):
        if self.dir:
            shutil.rmtree(self.dir)
        self.dir = None

@pytest.fixture(scope="module")
def tmpdir(request):
    td = TmpDir()
    request.addfinalizer(td.cleanup)
    return td.dir
