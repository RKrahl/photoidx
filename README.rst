|gh-test|

.. |gh-test| image:: https://img.shields.io/github/workflow/status/RKrahl/photo-tools/Run%20Test
   :target: https://github.com/RKrahl/photo-tools/actions/workflows/run-tests.yaml
   :alt: GitHub Workflow Status

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

+ Python 3.6 or newer.

Required library packages:

+ `setuptools`_

+ `PyYAML`_

+ `exif`_ >= 0.8.3

+ `PySide`_

Optional library packages:

+ `vignette`_ >= 4.3.0

  Needed to cache thumbnail images for the overview window.  If
  vignette is not available, everything will still work, but
  displaying the overview window may be significantly slower.

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


Copyright and License
---------------------

Copyright 2015–2022 Rolf Krahl

Licensed under the `Apache License`_, Version 2.0 (the "License"); you
may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.  See the License for the specific language governing
permissions and limitations under the License.


.. _setuptools: https://github.com/pypa/setuptools/
.. _PyYAML: https://github.com/yaml/pyyaml
.. _exif: https://github.com/TNThieding/exif
.. _PySide: https://wiki.qt.io/PySide
.. _vignette: https://github.com/hydrargyrum/vignette
.. _setuptools_scm: https://github.com/pypa/setuptools_scm/
.. _pytest: https://pytest.org/
.. _pytest-dependency: https://github.com/RKrahl/pytest-dependency
.. _distutils-pytest: https://github.com/RKrahl/distutils-pytest
.. _Installing Python Modules: https://docs.python.org/3/install/
.. _Apache License: https://www.apache.org/licenses/LICENSE-2.0
