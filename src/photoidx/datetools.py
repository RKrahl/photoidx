"""Helper functions for manipulating dates and times.

**Note**: This module might be useful independently of photoidx.  It
is included here because photoidx uses it internally, but it is not
considered to be part of the API.  Changes in this module are not
considered API changes of photoidx.  It may even be removed from
future versions of the photoidx distribution without further notice.
"""

import datetime
import re

_tz_re = re.compile(r'(?P<sign>[+-])(?P<hour>\d{2}):(?P<min>\d{2})')

def timedelta_round_to_minute(offs):
    """Round a timedelta object to whole minutes.
    """
    minutes = round(offs.total_seconds()/60)
    return datetime.timedelta(minutes=minutes)

def local_time_zone():
    """Get a time zone object corresponding to the local time.
    """
    now = datetime.datetime.now()
    # We'd need utcnow() here, but it is deprecated and will be
    # removed from future Python versions.
    utcnow = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    offs = now - utcnow
    return datetime.timezone(timedelta_round_to_minute(offs))

def str_to_tz(s):
    """Parse a string representation of a time zone to a timezone object.
    """
    m = _tz_re.fullmatch(s)
    if not m:
        raise ValueError("invalid time zone '%s'" % s)
    hour, minute = m.group('hour', 'min')
    offs = datetime.timedelta(hours=int(hour), minutes=int(minute))
    if m.group('sign') == '-':
        offs = -offs
    return datetime.timezone(offs)
