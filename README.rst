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

 + Python 2.7.  The package itself should also work with Python 3,
   but some prerequisites only support Python 2.

Required library packages:

 + `PyYAML`_

 + `gexiv2`_

 + `PySide`_

Optional library packages, only needed to run the test suite:

 + `pytest`_

 + `distutils-pytest`_


Installation
------------

photo-tools follows the standard Python conventions of packaging
source distributions.  See the documentation on `Installing Python
Modules`_ for details or to customize the install process.

  1. Download the sources, unpack, and change into the source
     directory.

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

Copyright 2015, 2016 Rolf Krahl

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
.. _pytest: http://pytest.org/
.. _distutils-pytest: https://github.com/RKrahl/distutils-pytest
.. _Installing Python Modules: https://docs.python.org/2.7/install/
