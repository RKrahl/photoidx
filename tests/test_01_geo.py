"""Test class GeoPosition.
"""

import re
import pytest
from photoidx.geo import GeoPosition


geopos_str_pattern = (r"^\s*(?P<lat>\d+).*(?P<latref>N|S),\s*"
                      r"(?P<lon>\d+).*(?P<lonref>E|W)\s*$")
geopos_str_re = re.compile(geopos_str_pattern)

class PositionData:

    def __init__(self, lat, lon, name):
        self.lat = lat
        self.latref = 'N' if lat >= 0 else 'S'
        self.lon = lon
        self.lonref = 'E' if lon >= 0 else 'W'
        self.name = name

    def as_pytest_param(self):
        return pytest.param(self, id=self.name)

# Example geo positions.  We want example points for all quarters of
# the earth sphere: N/E, N/W, S/E, S/W
pos_berlin = PositionData(52.51959, 13.40684, "berlin")
pos_philly = PositionData(39.94918, -75.14993, "philly")
pos_vfalls = PositionData(-17.92304, 25.84708, "vic_falls")
pos_sirius = PositionData(-22.80778, -47.05250, "sirius")


@pytest.mark.parametrize("pos", [
    pos_berlin.as_pytest_param(),
    pos_philly.as_pytest_param(),
    pos_vfalls.as_pytest_param(),
    pos_sirius.as_pytest_param(),
])
def test_geo_init(pos):
    """Test different options to initialize GeoPosition objects.
    """
    p_a = GeoPosition({pos.latref: abs(pos.lat), pos.lonref: abs(pos.lon)})
    p_b = GeoPosition("%f %s, %f %s"
                      % (abs(pos.lat), pos.latref, abs(pos.lon), pos.lonref))
    p_c = GeoPosition((pos.lat, pos.lon))
    assert (p_a.lat, p_a.lon) == pytest.approx((p_b.lat, p_b.lon))
    assert (p_a.lat, p_a.lon) == pytest.approx((p_c.lat, p_c.lon))
    assert (p_b.lat, p_b.lon) == pytest.approx((p_c.lat, p_c.lon))

@pytest.mark.parametrize("pos", [
    pos_berlin.as_pytest_param(),
    pos_philly.as_pytest_param(),
    pos_vfalls.as_pytest_param(),
    pos_sirius.as_pytest_param(),
])
def test_geo_str(pos):
    """Test string representations of GeoPosition objects.

    Refrain from verifying the resulting strings in detail, rather
    limit ourself to a cursory plausibility check.
    """
    p = GeoPosition((pos.lat, pos.lon))
    m = geopos_str_re.match(str(p))
    assert m
    assert int(m.group('lat')) == int(abs(pos.lat))
    assert m.group('latref') == pos.latref
    assert int(m.group('lon')) == int(abs(pos.lon))
    assert m.group('lonref') == pos.lonref
    m = geopos_str_re.match(p.floatstr())
    assert m
    assert int(m.group('lat')) == int(abs(pos.lat))
    assert m.group('latref') == pos.latref
    assert int(m.group('lon')) == int(abs(pos.lon))
    assert m.group('lonref') == pos.lonref
