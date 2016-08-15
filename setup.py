#! /usr/bin/python

from distutils.core import setup
try:
    from distutils.command.build_py import build_py_2to3 as build_py
    # Must disable the filter fixer.
    import lib2to3.refactor
    fixer_names = lib2to3.refactor.get_fixers_from_package('lib2to3.fixes')
    fixer_names.remove('lib2to3.fixes.fix_filter')
    build_py.fixer_names = fixer_names
except ImportError:
    # Python 2.x
    from distutils.command.build_py import build_py
try:
    import distutils_pytest
except ImportError:
    pass
import photo
import re

DOCLINES         = photo.__doc__.split("\n")
DESCRIPTION      = DOCLINES[0]
LONG_DESCRIPTION = "\n".join(DOCLINES[2:])
VERSION          = photo.__version__
AUTHOR           = photo.__author__
m = re.match(r"^(.*?)\s*<(.*)>$", AUTHOR)
(AUTHOR_NAME, AUTHOR_EMAIL) = m.groups() if m else (AUTHOR, None)


setup(
    name = "photo",
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    author = AUTHOR_NAME,
    author_email = AUTHOR_EMAIL,
    license = "Apache-2.0",
    requires = ["yaml"],
    packages = ["photo", "photo.qt"],
    scripts = ["photoidx.py", "imageview.py"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        ],
    cmdclass = {'build_py': build_py},
)

