"""Test the photoidx.datetools module.
"""

import datetime
import time
import pytest
import photoidx.datetools


# Fix some arbitrary time zones and a reference date
ACST = datetime.timezone(datetime.timedelta(hours=9, minutes=30))
JST = datetime.timezone(datetime.timedelta(hours=9))
EET = datetime.timezone(datetime.timedelta(hours=3))
CET = datetime.timezone(datetime.timedelta(hours=1))
CEST = datetime.timezone(datetime.timedelta(hours=2))
CST = datetime.timezone(datetime.timedelta(hours=-6))
ref_date = datetime.datetime(2023, 8, 21, 10, 53, 12, tzinfo=EET)


def test_rounded_timezone():
    """Test get_rounded_timezone().

    Note that the offest in the test is off by one second, which
    doesn't matter, since the time zone is rounded to the minute.
    """
    createDate = datetime.datetime(2024, 11, 17, 10, 55, 1)
    gpsDateTime = datetime.datetime(2024, 11, 17, 16, 55, 2)
    offs = createDate - gpsDateTime
    tz = photoidx.datetools.get_rounded_timezone(offs)
    assert tz == CST
    

def test_local_offs_tz():
    """Test get_local_offset_time_zone()
    """
    local_tz = CEST if time.localtime().tm_isdst else CET
    assert photoidx.datetools.get_local_offset_time_zone() == local_tz


@pytest.mark.parametrize("tzname, conv_date, utcoffset", [
    ("Asia/Tokyo",
     datetime.datetime(2023, 8, 21, 16, 53, 12, tzinfo=JST), 32400),
    ("+09:00",
     datetime.datetime(2023, 8, 21, 16, 53, 12, tzinfo=JST), 32400),
    ("+0900",
     datetime.datetime(2023, 8, 21, 16, 53, 12, tzinfo=JST), 32400),
    ("UTC+09:00",
     datetime.datetime(2023, 8, 21, 16, 53, 12, tzinfo=JST), 32400),
    ("UTC+0900",
     datetime.datetime(2023, 8, 21, 16, 53, 12, tzinfo=JST), 32400),
    ("Australia/Adelaide",
     datetime.datetime(2023, 8, 21, 17, 23, 12, tzinfo=ACST), 34200),
    ("+09:30",
     datetime.datetime(2023, 8, 21, 17, 23, 12, tzinfo=ACST), 34200),
    ("+0930",
     datetime.datetime(2023, 8, 21, 17, 23, 12, tzinfo=ACST), 34200),
    ("UTC+09:30",
     datetime.datetime(2023, 8, 21, 17, 23, 12, tzinfo=ACST), 34200),
    ("UTC+0930",
     datetime.datetime(2023, 8, 21, 17, 23, 12, tzinfo=ACST), 34200),
    ("America/Costa_Rica",
     datetime.datetime(2023, 8, 21, 1, 53, 12, tzinfo=CST), -21600),
    ("-06:00",
     datetime.datetime(2023, 8, 21, 1, 53, 12, tzinfo=CST), -21600),
    ("-0600",
     datetime.datetime(2023, 8, 21, 1, 53, 12, tzinfo=CST), -21600),
    ("UTC-06:00",
     datetime.datetime(2023, 8, 21, 1, 53, 12, tzinfo=CST), -21600),
    ("UTC-0600",
     datetime.datetime(2023, 8, 21, 1, 53, 12, tzinfo=CST), -21600),
    (None,
     datetime.datetime(2023, 8, 21, 9, 53, 12, tzinfo=CEST), 7200),
])
def test_gettz(tzname, conv_date, utcoffset):
    """Test gettz() and gettz_name().

    Test that all the different ways to spell the names are understood
    by gettz() and that it yields a tzinfo with the expected
    properties.  Furthermore, test that the name returned by
    gettz_name() is suitable to get the same (more precisely, an
    equal) tzinfo again.
    """
    tz = photoidx.datetools.gettz(tzname)
    cd = ref_date.astimezone(tz)
    assert cd == conv_date
    assert tz.utcoffset(cd).total_seconds() == utcoffset
    tzname2 = photoidx.datetools.gettz_name(tz)
    tz2 = photoidx.datetools.gettz(tzname2)
    assert tz2 == tz


def test_gettz_emtpy():
    """Test gettz() returns None if given an empty string as argument.
    """
    assert photoidx.datetools.gettz("") == None
