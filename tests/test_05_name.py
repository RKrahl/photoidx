"""Read and write an index having optional name attributes in it.
"""

import filecmp
import shutil
import pytest
import photo.index
from conftest import tmpdir, gettestdata

refindex = gettestdata("index-name.yaml")

@pytest.fixture(scope="module")
def imgdir(tmpdir):
    shutil.copy(refindex, str(tmpdir.joinpath(".index.yaml")))
    return tmpdir

def test_readwrite(imgdir):
    """Read the index file and write it out again.
    """
    with photo.index.Index(idxfile=imgdir) as idx:
        assert idx[0].name == "ginza.jpg"
        assert idx[1].name is None
        assert idx[3].name == "geisha.jpg"
        idx.write()
    idxfile = str(imgdir.joinpath(".index.yaml"))
    assert filecmp.cmp(refindex, idxfile), "index file differs from reference"
