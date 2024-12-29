"""Read legacy format index files.

The index file format has changed in the course of photoidx versions.
The versions of this file format are numbered independently of the
version numbers for the photoidx package.  The current index file
format version is 1.0.  Previous versions didn't have an explicit
version number but have been retroactivly denominated as versions 0.1
and 0.4 respectively.

photoidx still reads legacy files and transparently converts them to
the new format.  This feature is tested in this module.
"""

from packaging.version import Version
import shutil
import pytest
import photoidx.index
from conftest import tmpdir, gettestdata, index_cmp

testimgs = [
    "dsc_4623.jpg", "dsc_4664.jpg", "dsc_4831.jpg",
    "dsc_5126.jpg", "dsc_5167.jpg"
]
testimgfiles = [ gettestdata(i) for i in testimgs ]

legacyindex = {
    "0.1": gettestdata("index-legacy-0_1.yaml"),
    "0.4": gettestdata("index-legacy-0_4.yaml"),
}
refindex = gettestdata("index-nocomment.yaml")

@pytest.mark.parametrize("version", legacyindex.keys())
def test_legacyconvert(tmpdir, version):
    """Read different legacy files and convert them to the current version.
    """
    workdir = tmpdir / version
    workdir.mkdir()
    for fname in testimgfiles:
        shutil.copy(fname, workdir)
    idxfile = workdir / ".index.yaml"
    shutil.copy(legacyindex[version], idxfile)
    # reading and writing the index transparantly converts it.
    with photoidx.index.Index(idxfile=workdir) as idx:
        assert idx.version == Version(version)
        idx.write()
    assert index_cmp(idxfile, refindex), "index file differs from reference"


def test_legacy_mix_checksums(tmpdir):
    """Pathologic case of a legacy index having inconsistent hash algorithms.

    The file reader selects the common set of hash algorithms present
    in all index items for the Checksums header upon conversion.
    """
    workdir = tmpdir / "checksums"
    workdir.mkdir()
    for fname in testimgfiles:
        shutil.copy(fname, workdir)
    idxfile = workdir / ".index.yaml"
    shutil.copy(gettestdata("index-legacy-checksums.yaml"), idxfile)
    with photoidx.index.Index(idxfile=workdir) as idx:
        assert set(idx.checksums) == {"sha1", "sha256"}
