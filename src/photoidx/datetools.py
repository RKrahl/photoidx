"""Helper functions for manipulating dates and times.

**Note**: This module might be useful independently of photoidx.  It
is included here because photoidx uses it internally, but it is not
considered to be part of the API.  Changes in this module are not
considered API changes of photoidx.  It may even be removed from
future versions of the photoidx distribution without further notice.
"""

import datetime
from pathlib import Path
import re
try:
    import dateutil.tz
    _have_dateutil_tz = True
except ImportError:
    _have_dateutil_tz = False

_tz_offs_re = re.compile(r'''
    (?:UTC)?
    (?P<sign>[+-])
    (?P<hour>\d{2})
    :?
    (?P<min>\d{2})
''', re.X)
_tzfile_repr_re = re.compile(r'\w+\(\'(?P<path>[/a-zA-Z0-9_]+)\'\)')


def get_rounded_timezone(offs):
    """Create a timezone object from an offset rounded to whole minutes.
    """
    minutes = round(offs.total_seconds()/60)
    return datetime.timezone(datetime.timedelta(minutes=minutes))


def get_local_offset_time_zone():
    """Get a time zone object corresponding to the local time.
    """
    now = datetime.datetime.now()
    # We'd need utcnow() here, but it is deprecated and will be
    # removed from future Python versions.
    utcnow = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    return get_rounded_timezone(now - utcnow)


def gettz(name=None):
    """Get a time zone from a string representation.
    """
    if name is not None:
        if not name:
            return None
        m = _tz_offs_re.fullmatch(name)
        if m:
            hour, minute = m.group('hour', 'min')
            offs = datetime.timedelta(hours=int(hour), minutes=int(minute))
            if m.group('sign') == '-':
                offs = -offs
            return datetime.timezone(offs)
    if _have_dateutil_tz:
        tz = dateutil.tz.gettz(name)
        if tz:
            return tz
    elif name is None:
        return get_local_offset_time_zone()
    raise ValueError("invalid time zone '%s'" % name)


def gettz_name(tz):
    """Get the name from a dateutil.tz.tzfile object.

    This is supposed to be the inverse of gettz().
    """
    if _have_dateutil_tz and isinstance(tz, dateutil.tz.tzfile):
        # Note: this code probably does not work on Windows
        m = _tzfile_repr_re.match(repr(tz))
        if m:
            path = Path(m.group('path')).resolve()
            for zi_dir in dateutil.tz.TZPATHS:
                try:
                    return str(path.relative_to(zi_dir))
                except ValueError:
                    continue
    elif isinstance(tz, datetime.timezone):
        return str(tz)
    raise ValueError("invalid time zone object %r" % tz)
