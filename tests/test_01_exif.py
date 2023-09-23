"""Use the photoidx.exif module to read EXIF tags from image files.

For the time being, only consider the Orientation tag.  More tests
considering other tags may be added later.
"""

from pathlib import Path
import pytest
import photoidx.exif
from conftest import gettestdata

@pytest.mark.parametrize("o", range(1, 9))
def test_exif_orientation(o):
    testimg = "dsc_1190-o%d.jpg" % o
    filename = Path(gettestdata(testimg))
    exifdata = photoidx.exif.Exif(filename)
    orientation = exifdata.orientation
    assert orientation == o
    assert str(orientation) == photoidx.exif.Orientation.OrientationLabels[o]
