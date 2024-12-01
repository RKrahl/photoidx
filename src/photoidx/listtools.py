"""Some useful list classes.

**Note**: This module might be useful independently of photoidx.  It
is included here because photoidx uses it internally, but it is not
considered to be part of the API.  Changes in this module are not
considered API changes of photoidx.  It may even be removed from
future versions of the photoidx distribution without further notice.
"""

from collections.abc import MutableSequence

class LazyList(MutableSequence):
    """A list generated lazily from an iterable.

    LazyList provides list access to the sequence of elements from the
    iterable.  Elements are taken out lazily.  That means, the
    elements are taken from the iterable not before they are actually
    accessed.  Once taken out, the elements are stored in a
    conventional list in order to provide random access.  The string
    representation operator of LazyList only displays the elements
    taken out of the iterable so far.

    Note: if the list is accessed at the end using negative indices,
    all elements are taken from the iterable before returning the
    result.  Some operations implicitly access the list at the end and
    thus take all elements from the iterable.  These operations
    include `len()` and `append()`.  Do not access the list at the end
    using negativ indices or append to the list if you cannot afford
    to take all elements out of the iterable.

    >>> l = LazyList((0, 1, 2, 3, 4))
    >>> l
    []
    >>> l[1]
    1
    >>> l
    [0, 1]
    >>> del l[1]
    >>> l
    [0]
    >>> l[1]
    2
    >>> l
    [0, 2]
    >>> l[8]
    Traceback (most recent call last):
      ...
    IndexError: list index out of range
    >>> l
    [0, 2, 3, 4]
    >>> l = LazyList((0, 1, 2, 3, 4))
    >>> l[-2]
    3
    >>> l
    [0, 1, 2, 3, 4]
    >>> l = LazyList((0, 1, 2, 3, 4))
    >>> list(l) == [0, 1, 2, 3, 4]
    True
    >>> l
    [0, 1, 2, 3, 4]
    >>> l = LazyList((0, 1, 2, 3, 4))
    >>> len(l)
    5
    >>> l
    [0, 1, 2, 3, 4]
    >>> l = LazyList((0, 1, 2, 3, 4))
    >>> l.append(5)
    >>> l
    [0, 1, 2, 3, 4, 5]
    >>> def naturals():
    ...     n = 0
    ...     while True:
    ...         yield n
    ...         n += 1
    ... 
    >>> l = LazyList(naturals())
    >>> l[1]
    1
    >>> l
    [0, 1]
    >>> l[4:2:-1]
    [4, 3]
    >>> l
    [0, 1, 2, 3, 4]
    >>> l[8]
    8
    >>> l
    [0, 1, 2, 3, 4, 5, 6, 7, 8]
    >>> l[17:11]
    []
    >>> l
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> l = LazyList(naturals())
    >>> l
    []
    >>> bool(l)
    True
    >>> l
    [0]
    >>> l = LazyList((0, 1, 2, 3, 4, 5, 6))
    >>> l.index(1)
    1
    >>> l
    [0, 1]
    >>> l.index(2, 1)
    2
    >>> l
    [0, 1, 2]
    >>> l.index(2, 3, 5)
    Traceback (most recent call last):
      ...
    ValueError: 2 is not in list
    >>> l
    [0, 1, 2, 3, 4]
    >>> l.index(2, 3)
    Traceback (most recent call last):
      ...
    ValueError: 2 is not in list
    >>> l
    [0, 1, 2, 3, 4, 5, 6]

    """

    def __init__(self, iterable):
        self.iterable = iter(iterable)
        self.elements = []

    def _access_next(self):
        """Take out the next element from the iterable.
        Raise StopIteration if the iterable is exhausted.
        """
        v = next(self.iterable)
        self.elements.append(v)
        return v

    def _access(self, index):
        """Try to take out the elements covered by index from the iterable.
        The argument may be an int or a slice.  Do not raise an error,
        even if not enough elements can be delivered by the iterable.
        """
        m = 0
        if isinstance(index, int):
            m = index + 1 if index >= 0 else -1
        elif isinstance(index, slice):
            if index.step is not None and index.step < 0:
                m = index.start + 1 if index.start >= 0 else -1
            else:
                m = index.stop if index.stop >= 0 else -1
        while len(self.elements) < m or m < 0:
            try:
                self._access_next()
            except StopIteration:
                break

    def __len__(self):
        self._access(-1)
        return len(self.elements)

    def __getitem__(self, index):
        self._access(index)
        return self.elements.__getitem__(index)

    def __setitem__(self, index, value):
        self._access(index)
        self.elements.__setitem__(index, value)

    def __delitem__(self, index):
        self._access(index)
        self.elements.__delitem__(index)

    def index(self, value, *args):
        try:
            startidx = args[0]
        except IndexError:
            startidx = 0
        try:
            endidx = args[1]
        except IndexError:
            endidx = None
        self._access(startidx)
        try:
            return self.elements.index(value, *args)
        except ValueError:
            i = len(self.elements)
            while True:
                if endidx and i >= endidx:
                    raise ValueError("%s is not in list" % repr(value))
                try:
                    v = self._access_next()
                    if v == value:
                        return i
                    i += 1
                except StopIteration:
                    raise ValueError("%s is not in list" % repr(value))

    def insert(self, index, value):
        self._access(index)
        self.elements.insert(index, value)

    def append(self, value):
        self._access(-1)
        self.elements.append(value)

    def __bool__(self):
        self._access(0)
        return bool(self.elements)

    def __str__(self):
        return str(self.elements)

    def __repr__(self):
        return repr(self.elements)
