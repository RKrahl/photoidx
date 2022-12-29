Changelog
=========


0.10.0 (2022-12-29)
~~~~~~~~~~~~~~~~~~~

New features
------------

+ `#43`_, `#57`_: Keep the center of current display stable, if
  possible when zooming in or out in :ref:`imageview`.

Incompatible changes
--------------------

+ `#52`_, `#53`_: Rename the package from ``photo`` to ``photoidx``.

Internal changes
----------------

+ `#34`_, `#55`_: Upgrade to Pyside2.
+ `#48`_, `#56`_, `#58`_: Move from `gexiv2`_ to `ExifRead`_.
+ `#51`_: Review build tool chain.
+ `#47`_, `#50`_: Use `setuptools_scm`_ to manage the version number.

Bug fixes and minor changes
---------------------------

+ `#54`_: Check whether vignette has any thumbnailer backend.
+ `#49`_: Fix :exc:`DeprecationWarning` about importing the ABCs from
  :mod:`collections`.

.. _#34: https://github.com/RKrahl/photoidx/issues/34
.. _#43: https://github.com/RKrahl/photoidx/issues/43
.. _#47: https://github.com/RKrahl/photoidx/issues/47
.. _#48: https://github.com/RKrahl/photoidx/issues/48
.. _#49: https://github.com/RKrahl/photoidx/pull/49
.. _#50: https://github.com/RKrahl/photoidx/pull/50
.. _#51: https://github.com/RKrahl/photoidx/pull/51
.. _#52: https://github.com/RKrahl/photoidx/issues/52
.. _#53: https://github.com/RKrahl/photoidx/pull/53
.. _#54: https://github.com/RKrahl/photoidx/pull/54
.. _#55: https://github.com/RKrahl/photoidx/pull/55
.. _#56: https://github.com/RKrahl/photoidx/issues/56
.. _#57: https://github.com/RKrahl/photoidx/pull/57
.. _#58: https://github.com/RKrahl/photoidx/pull/58


0.9.3 (2020-05-03)
~~~~~~~~~~~~~~~~~~

Bug fixes and minor changes
---------------------------

+ `#46`_: Fix :exc:`yaml.YAMLLoadWarning`.

.. _#46: https://github.com/RKrahl/photoidx/issues/46


0.9.2 (2019-09-01)
~~~~~~~~~~~~~~~~~~

Bug fixes and minor changes
---------------------------

+ `#45`_: update the code limiting the `vignette`_ thumbnailer
  backends to use.

.. _#45: https://github.com/RKrahl/photoidx/pull/45


0.9.1 (2019-08-21)
~~~~~~~~~~~~~~~~~~

Bug fixes and minor changes
---------------------------

+ `#44`_: opening the filter options dialog fails with
  :exc:`TypeError`.

.. _#44: https://github.com/RKrahl/photoidx/issues/44


0.9.0 (2019-08-05)
~~~~~~~~~~~~~~~~~~

New features
------------

+ `#39`_: Review behavior of :ref:`imageview` concerning writing the
  index: the index is not automatically written to disk any more after
  each modification, but the user need to explicitly save it.
  :ref:`imageview` may create a new index if started with the
  ``--create`` command line flag.

Incompatible changes
--------------------

+ Drop support for Python 2.  Require Python 3.4 or newer.

+ Use :class:`pathlib.Path` rather then :class:`str` in
  :attr:`photoidx.idxitem.IdxItem.filename`.  Switch to :mod:`pathlib`
  for most internal representation of filesystem paths.  As a side
  effect, the semantic of file paths may be taken somewhat more
  coherent and strict now at some places.

Bug fixes and minor changes
---------------------------

+ `#42`_: :ref:`imageview` may inadvertently create an image index.

.. _#39: https://github.com/RKrahl/photoidx/issues/39
.. _#42: https://github.com/RKrahl/photoidx/issues/42


0.8.2 (2019-01-01)
~~~~~~~~~~~~~~~~~~

Bug fixes and minor changes
---------------------------

+ `#41`_: Setting filter options in
  :class:`~photoidx.qt.imageViewer.ImageViewer` fails with
  :exc:`IndexError` if current filter selects no image.

.. _#41: https://github.com/RKrahl/photoidx/issues/41


0.8.1 (2019-01-01)
~~~~~~~~~~~~~~~~~~

Bug fixes and minor changes
---------------------------

+ `#40`_: :exc:`TypeError` is raised when trying to read a non
  existing index file.

.. _#40: https://github.com/RKrahl/photoidx/issues/40


0.8 (2018-12-31)
~~~~~~~~~~~~~~~~

New features
------------

+ `#31`_: Implement modifying the current filter in
  :class:`~photoidx.qt.imageViewer.ImageViewer`.

+ `#30`_: Protect the index file against conflicting concurrent access
  using file system locking.

+ `#32`_: Add a ``stats`` command line interface subcommand.

+ `#20`_: Add a preferred order.  Add actions to the GUI to push
  images back and forth in the image order.

Incompatible changes
--------------------

+ `#35`_: Change the sematic of the ``--date`` command line option to
  :ref:`photo-idx` and :ref:`imageview`: when an interval is given as
  argument, the end time is taken exclusively.
  E.g. ``--date=2015-03-14--2015-03-15`` excludes images taken on
  March 15.

Bug fixes and minor changes
---------------------------

+ `#36`_: Opening the overview images fails with :exc:`IndexError` if
  no image is shown.

+ `#37`_: :exc:`AttributeError` is raised when calling :ref:`photo-idx`
  without arguments.

+ Add method :meth:`photoidx.index.Index.extend_dir`.

+ :meth:`photoidx.index.Index.index` now supports the full variant
  having start and end index arguments.

.. _#20: https://github.com/RKrahl/photoidx/issues/20
.. _#30: https://github.com/RKrahl/photoidx/issues/30
.. _#31: https://github.com/RKrahl/photoidx/issues/31
.. _#32: https://github.com/RKrahl/photoidx/issues/32
.. _#35: https://github.com/RKrahl/photoidx/issues/35
.. _#36: https://github.com/RKrahl/photoidx/issues/36
.. _#37: https://github.com/RKrahl/photoidx/issues/37


0.7 (2017-12-31)
~~~~~~~~~~~~~~~~

New features
------------

+ `#21`_: Add more information to the info window.

+ `#27`_: Set default scale in
  :class:`~photoidx.qt.imageViewer.ImageViewer` such that the first
  image just fits the maximum window size.

Bug fixes and minor changes
---------------------------

+ `#28`_: use `pytest-dependency`_ to mark dependencies in the test
  suite.

.. _#21: https://github.com/RKrahl/photoidx/issues/21
.. _#27: https://github.com/RKrahl/photoidx/issues/27
.. _#28: https://github.com/RKrahl/photoidx/issues/28


0.6 (2017-05-22)
~~~~~~~~~~~~~~~~

New features
------------

+ `#24`_: Add an overview window.

Bug fixes and minor changes
---------------------------

+ `#25`_: :class:`~photoidx.qt.imageViewer.ImageViewer` should
  remember rotation.

+ `#22`_: Unwanted unicode marker for tags in the index.

+ `#26`_: Get rid of :exc:`gi.PyGIWarning`.

+ Add an optional attribute :attr:`photoidx.idxitem.IdxItem.name`.  Use
  it as the title of the :class:`~photoidx.qt.imageViewer.ImageViewer`
  window if set.

.. _#22: https://github.com/RKrahl/photoidx/issues/22
.. _#24: https://github.com/RKrahl/photoidx/issues/24
.. _#25: https://github.com/RKrahl/photoidx/issues/25
.. _#26: https://github.com/RKrahl/photoidx/issues/26


0.5 (2016-08-22)
~~~~~~~~~~~~~~~~

New features
------------

+ `#19`_: Manage a persistent selection.

+ `#17`_: Speed up start of :ref:`imageview` when building in memory
  index for many files.

+ `#18`_: Add an image info window in :ref:`imageview`.

+ Do not throw an error in :ref:`imageview` if an image cannot be
  read, proceed to the next one instead.

Internal changes
----------------

+ Do not change directory when reading the image directory.

.. _#17: https://github.com/RKrahl/photoidx/issues/17
.. _#18: https://github.com/RKrahl/photoidx/issues/18
.. _#19: https://github.com/RKrahl/photoidx/issues/19


0.4 (2016-04-12)
~~~~~~~~~~~~~~~~

New features
------------

+ `#4`_: Add option to :ref:`photo-idx` to add missing images to an
  index.

+ `#10`_: Allow setting of new tags in :ref:`imageview`.

+ `#11`_: :ref:`imageview` should be able to work without an index.

+ `#5`_: Allow a date interval as argument to ``--date``.

+ `#12`_: Allow configuration of the type of checksum to be
  calculated.

Incompatible changes
--------------------

+ The index file format has changed.  :ref:`photo-idx` and
  :ref:`imageview` are able to read the old format and convert the
  file silently to the new format when writing it back.  But the tools
  from earlier versions will not fully work with the new format files.

Internal changes
----------------

+ `#1`_: Add a test suite.

+ `#3`_: Move from pyexiv2 to `gexiv2`_.

Bug fixes and minor changes
---------------------------

+ `#6`_: :ref:`imageview` crashes with :exc:`ZeroDivisionError` if no
  tags are set in the index.

+ `#13`_: :ref:`imageview` fails with :exc:`RuntimeError` if
  ``--directory`` option is used.

+ `#15`_: :ref:`photo-idx` ``create`` raises :exc:`KeyError` if
  exiftags are not present in an image.

+ `#9`_: Sort the tags when writing the index to a file.

.. _#1: https://github.com/RKrahl/photoidx/issues/1
.. _#3: https://github.com/RKrahl/photoidx/issues/3
.. _#4: https://github.com/RKrahl/photoidx/issues/4
.. _#5: https://github.com/RKrahl/photoidx/issues/5
.. _#6: https://github.com/RKrahl/photoidx/issues/6
.. _#9: https://github.com/RKrahl/photoidx/issues/9
.. _#10: https://github.com/RKrahl/photoidx/issues/10
.. _#11: https://github.com/RKrahl/photoidx/issues/11
.. _#12: https://github.com/RKrahl/photoidx/issues/12
.. _#13: https://github.com/RKrahl/photoidx/issues/13
.. _#15: https://github.com/RKrahl/photoidx/issues/15


0.3 (2016-01-02)
~~~~~~~~~~~~~~~~

New features
------------

+ Add image viewer.

+ Add ``--date`` command line argument to select images.

+ Add command line arguments ``--gpspos`` and ``--gpsradius`` to
  select images by GPS position.

+ Improve semantics in the ``--tags`` command line argument: Add
  exclamation mark to negate tags and allow specifying an empty tag
  list selecting only untagged images.


0.2 (2015-10-21)
~~~~~~~~~~~~~~~~

New features
------------

+ Add ``lstags`` sub command.


0.1 (2015-09-19)
~~~~~~~~~~~~~~~~

Initial version


.. _ExifRead: https://github.com/ianare/exif-py
.. _setuptools_scm: https://github.com/pypa/setuptools_scm/
.. _vignette: https://github.com/hydrargyrum/vignette
.. _pytest-dependency: https://github.com/RKrahl/pytest-dependency
.. _gexiv2: https://wiki.gnome.org/Projects/gexiv2
