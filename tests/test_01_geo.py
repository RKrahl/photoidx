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

    @staticmethod
    def as_pytest_param(*args):
        return pytest.param(*args, id="-".join(a.name for a in args))

# Example geo positions.  We want example points for all quarters of
# the earth sphere: N/E, N/W, S/E, S/W
pos_berlin = PositionData(52.51959, 13.40684, "berlin")
pos_philly = PositionData(39.94918, -75.14993, "philly")
pos_vfalls = PositionData(-17.92304, 25.84708, "vic_falls")
pos_sirius = PositionData(-22.80778, -47.05250, "sirius")
# and we want a couple of points that are close to each other
pos_spree1 = PositionData(51.00971, 14.64958, "spree1")
pos_spree2 = PositionData(50.98313, 14.61911, "spree2")
pos_spree3 = PositionData(50.98752, 14.60632, "spree3")


@pytest.mark.parametrize("pos", [
    PositionData.as_pytest_param(pos_berlin),
    PositionData.as_pytest_param(pos_philly),
    PositionData.as_pytest_param(pos_vfalls),
    PositionData.as_pytest_param(pos_sirius),
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
    PositionData.as_pytest_param(pos_berlin),
    PositionData.as_pytest_param(pos_philly),
    PositionData.as_pytest_param(pos_vfalls),
    PositionData.as_pytest_param(pos_sirius),
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
    # The value of floatstr() should be usable as argument to create a
    # new GeoPosition instance
    p1 = GeoPosition(p.floatstr())
    assert (p1.lat, p1.lon) == pytest.approx((p.lat, p.lon))

@pytest.mark.parametrize("pos1, pos2", [
    PositionData.as_pytest_param(pos_berlin, pos_vfalls),
    PositionData.as_pytest_param(pos_vfalls, pos_philly),
    PositionData.as_pytest_param(pos_philly, pos_berlin),
    PositionData.as_pytest_param(pos_berlin, pos_spree1),
    PositionData.as_pytest_param(pos_spree1, pos_spree2),
    PositionData.as_pytest_param(pos_spree2, pos_spree3),
])
def test_geo_center_dist(pos1, pos2):
    """Simple test for distance and centroid for GeoPosition objects.

    The centroid of two points should be the point having half the
    distance to either point.
    """
    p1 = GeoPosition((pos1.lat, pos1.lon))
    p2 = GeoPosition((pos2.lat, pos2.lon))
    d = (p1 - p2) / 2
    c = GeoPosition.centroid((p1, p2))
    assert (p1 - c) == pytest.approx(d)
    assert (p2 - c) == pytest.approx(d)

@pytest.mark.parametrize("pos1, pos2, pos3", [
    PositionData.as_pytest_param(pos_spree1, pos_spree2, pos_spree3),
])
def test_geo_triangle_centroid(pos1, pos2, pos3):
    """A complex triangle centroid test.

    Consider a triangle and a second triangle defined by the centroids
    of the three edges of the first triangle.  Both triangles should
    have the same centroid.  This test only works for positions that
    are not to far from each other, otherwise the inaccuracies from
    projecting the centroids to the earth's surface become to large.
    """
    p1 = GeoPosition((pos1.lat, pos1.lon))
    p2 = GeoPosition((pos2.lat, pos2.lon))
    p3 = GeoPosition((pos3.lat, pos3.lon))
    c0 = GeoPosition.centroid((p1, p2, p3))
    e1 = GeoPosition.centroid((p2, p3))
    e2 = GeoPosition.centroid((p1, p3))
    e3 = GeoPosition.centroid((p1, p2))
    c1 = GeoPosition.centroid((e1, e2, e3))
    assert (c1.lat, c1.lon) == pytest.approx((c0.lat, c0.lon))
