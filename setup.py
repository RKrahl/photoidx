#! /usr/bin/python

from distutils.core import setup
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
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        ],
)

