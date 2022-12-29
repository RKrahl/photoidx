|gh-test| |pypi|

.. |gh-test| image:: https://img.shields.io/github/actions/workflow/status/RKrahl/photoidx/run-tests.yaml?branch=develop
   :target: https://github.com/RKrahl/photoidx/actions/workflows/run-tests.yaml
   :alt: GitHub Workflow Status

.. |pypi| image:: https://img.shields.io/pypi/v/photoidx
   :target: https://pypi.org/project/photoidx/
   :alt: PyPI version

photoidx - Maintain indices for photo collections
=================================================

This package maintains indices for photo collections.  The index is
stored as a YAML file and contains metadata and tags describing the
photos.  The photos are accessed read only.

The package provides a command line tool to create and manipulate the
index and a graphical image viewer.


System requirements
-------------------

Python:

+ Python 3.6 or newer.

Required library packages:

+ `setuptools`_

+ `PyYAML`_

+ `ExifRead`_ >= 2.2.0

+ `PySide2`_

Optional library packages:

+ `vignette`_ >= 4.3.0

  Needed to cache thumbnail images for the overview window.  If
  vignette is not available, everything will still work, but
  displaying the overview window may be significantly slower.

+ vignette needs at least one thumbnail backend, either `Pillow`_ or
  `PyQt5`_.  If no suitable backend is found, vignette will be
  disabled in photoidx.

+ `setuptools_scm`_

  The version number is managed using this package.  All source
  distributions add a static text file with the version number and
  fall back using that if `setuptools_scm` is not available.  So this
  package is only needed to build out of the plain development source
  tree as cloned from GitHub.

+ `pytest`_ >= 3.0.0

  Only needed to run the test suite.

+ `pytest-dependency`_

  Only needed to run the test suite.  (Actually, you can run the test
  suite even without it, but dependencies between tests will be
  ignored then.)

+ `distutils-pytest`_

  Only needed to run the test suite.


Install instructions
--------------------

Note that the GUI of photoidx requires PySide2, but the installation
of PySide2 using pip seem to be thoroughly broken.  That is why that
dependency is deliberately omitted in the setup script of photoidx.
You need to install PySide2 independently before installing photoidx.
It is advisable to install PySide2 using the package manager of your
operating system rather than from PyPI.

Furthermore, you may want to install vignette along with a thumbnail
backend to enable cached thumbnails in the overview window.  This also
needs to be installed independently.

Release packages of photoidx are published in the `Python Package
Index (PyPI)`__.

.. __: `PyPI site`_

Installation using pip
......................

You can install photoidx from PyPI using pip::

  $ pip install photoidx

Installation from the source distribution
.........................................

Steps to manually build from the source distribution:

1. Download the sources, unpack, and change into the source directory.

2. Build::

     $ python setup.py build

3. Test (optional)::

     $ python setup.py test

4. Install::

     $ python setup.py install

The last step might require admin privileges in order to write into
the site-packages directory of your Python installation.

Note that this still requires a release version of the source
distribution.  The development sources that you may clone from the
source repository on GitHub is missing some files that are dynamically
created during the release.


Copyright and License
---------------------

Copyright 2015–2022 Rolf Krahl

Licensed under the `Apache License`_, Version 2.0 (the "License"); you
may not use this package except in compliance with the License.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.  See the License for the specific language governing
permissions and limitations under the License.


.. _setuptools: https://github.com/pypa/setuptools/
.. _PyYAML: https://github.com/yaml/pyyaml
.. _ExifRead: https://github.com/ianare/exif-py
.. _PySide2: https://www.pyside.org/
.. _vignette: https://github.com/hydrargyrum/vignette
.. _Pillow: https://python-pillow.org/
.. _PyQt5: https://www.riverbankcomputing.com/software/pyqt/
.. _setuptools_scm: https://github.com/pypa/setuptools_scm/
.. _pytest: https://pytest.org/
.. _pytest-dependency: https://github.com/RKrahl/pytest-dependency
.. _distutils-pytest: https://github.com/RKrahl/distutils-pytest
.. _PyPI site: https://pypi.org/project/photoidx/
.. _Apache License: https://www.apache.org/licenses/LICENSE-2.0
