Install instructions
====================

Release packages of photoidx are published in the `Python Package
Index (PyPI)`__.  See :ref:`install-using-pip` for the short version
of the install instructions.

.. __: `PyPI site`_


System requirements
-------------------

Python
......

+ Python 3.6 or newer.

Required library packages
.........................

The following packages are required to install and use photoidx.

+ `setuptools`_

+ `packaging`_

+ `PyYAML`_

+ `ExifRead`_ >= 2.2.0

+ `PySide2`_, see note below

Optional library packages
.........................

These packages are only needed to use certain extra features.  They
are not required to install and use the package:

+ `vignette`_ >= 4.3.0

  Needed to cache thumbnail images for the overview window.  If
  vignette is not available, everything will still work, but
  displaying the overview window may be significantly slower.

+ vignette needs at least one thumbnail backend, for instance
  `Pillow`_ >= 6.0 or `PyQt5`_, see the vignette documentation for
  details.  If no suitable backend is found, vignette will be disabled
  in photoidx.

+ `setuptools_scm`_

  The version number is managed using this package.  All source
  distributions add a static text file with the version number and
  fall back using that if setuptools_scm is not available.  So this
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

PySide2
.......

Note that the GUI of photoidx requires PySide2.  But PySide2 should be
built using the Qt library installed in your system.  Therefore it is
advisable to install it using the package manager of your operating
system, rather than from PyPI.  This needs to be done before trying to
install photoidx.


Installation
------------

.. _install-using-pip:

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


.. _PyPI site: https://pypi.org/project/photoidx/
.. _setuptools: https://github.com/pypa/setuptools/
.. _packaging: https://github.com/pypa/packaging/
.. _PyYAML: https://github.com/yaml/pyyaml/
.. _ExifRead: https://github.com/ianare/exif-py
.. _PySide2: https://www.pyside.org/
.. _vignette: https://github.com/hydrargyrum/vignette
.. _Pillow: https://python-pillow.org/
.. _PyQt5: https://www.riverbankcomputing.com/software/pyqt/
.. _setuptools_scm: https://github.com/pypa/setuptools_scm/
.. _pytest: https://pytest.org/
.. _pytest-dependency: https://github.com/RKrahl/pytest-dependency
.. _distutils-pytest: https://github.com/RKrahl/distutils-pytest
