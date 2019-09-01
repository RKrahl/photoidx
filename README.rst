photo-tools - Tools for photo collections
=========================================

This package provides tools for the management of photo collections.
It maintains an index of the photos in a text file.  All metadata is
stored in this index file in YAML format, the photos are accessed read
only.

The package provides a command line tool to manipulate the metadata
and a graphical image viewer.


System requirements
-------------------

Python:

+ Python 3.4 or newer.

Required library packages:

+ `PyYAML`_

+ `gexiv2`_

+ `PySide`_

Optional library packages:

+ `vignette`_ >= 4.3.0

  Needed to cache thumbnail images for the overview window.  If
  vignette is not available, everything will still work, but
  displaying the overview window may be significantly slower.

+ `pytest`_

  Only needed to run the test suite.

+ `pytest-dependency`_

  Only needed to run the test suite.  (Actually, you can run the test
  suite even without it, but dependencies between tests will be
  ignored then.)

+ `distutils-pytest`_

  Only needed to run the test suite.


Installation
------------

This package uses the distutils Python standard library package and
follows its conventions of packaging source distributions.  See the
documentation on `Installing Python Modules`_ for details or to
customize the install process.

1. Download the sources, unpack, and change into the source directory.

2. Build::

     $ python setup.py build

3. Test (optional)::

     $ python setup.py test

4. Install::

     $ python setup.py install

The last step might require admin privileges in order to write into
the site-packages directory of your Python installation.


Copyright and License
---------------------

Copyright 2015-2019 Rolf Krahl

Licensed under the Apache License, Version 2.0 (the "License"); you
may not use this file except in compliance with the License.  You may
obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.  See the License for the specific language governing
permissions and limitations under the License.



.. _PyYAML: http://pyyaml.org/wiki/PyYAML
.. _gexiv2: https://wiki.gnome.org/Projects/gexiv2
.. _PySide: http://qt-project.org/wiki/PySide
.. _vignette: https://github.com/hydrargyrum/vignette
.. _pytest: http://pytest.org/
.. _pytest-dependency: https://github.com/RKrahl/pytest-dependency
.. _distutils-pytest: https://github.com/RKrahl/distutils-pytest
.. _Installing Python Modules: https://docs.python.org/2.7/install/
