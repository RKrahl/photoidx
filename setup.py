"""Maintain indices for photo collections

This package maintains indices for photo collections.  The index is
stored as a YAML file and contains metadata and tags describing the
photos.  The photos are accessed read only.
"""

import setuptools
from setuptools import setup
import setuptools.command.build_py
import distutils.command.sdist
from distutils import log
from glob import glob
from pathlib import Path
import string
try:
    import distutils_pytest
    cmdclass = distutils_pytest.cmdclass
except (ImportError, AttributeError):
    cmdclass = dict()
try:
    import setuptools_scm
    version = setuptools_scm.get_version()
except (ImportError, LookupError):
    try:
        import _meta
        version = _meta.__version__
    except ImportError:
        log.warn("warning: cannot determine version number")
        version = "UNKNOWN"

docstring = __doc__


class meta(setuptools.Command):

    description = "generate meta files"
    user_options = []
    init_template = '''"""%(doc)s"""

__version__ = "%(version)s"
'''
    meta_template = '''
__version__ = "%(version)s"
'''

    def initialize_options(self):
        self.package_dir = None

    def finalize_options(self):
        self.package_dir = {}
        if self.distribution.package_dir:
            for name, path in self.distribution.package_dir.items():
                self.package_dir[name] = convert_path(path)

    def run(self):
        values = {
            'version': self.distribution.get_version(),
            'doc': docstring
        }
        try:
            pkgname = self.distribution.packages[0]
        except IndexError:
            log.warn("warning: no package defined")
        else:
            pkgdir = Path(self.package_dir.get(pkgname, pkgname))
            if not pkgdir.is_dir():
                pkgdir.mkdir()
            with (pkgdir / "__init__.py").open("wt") as f:
                print(self.init_template % values, file=f)
        with Path("_meta.py").open("wt") as f:
            print(self.meta_template % values, file=f)


# Note: Do not use setuptools for making the source distribution,
# rather use the good old distutils instead.
# Rationale: https://rhodesmill.org/brandon/2009/eby-magic/
class sdist(distutils.command.sdist.sdist):
    def run(self):
        self.run_command('meta')
        super().run()
        subst = {
            "version": self.distribution.get_version(),
            "url": self.distribution.get_url(),
            "description": docstring.split("\n")[0],
            "long_description": docstring.split("\n", maxsplit=2)[2].strip(),
        }
        for spec in glob("*.spec"):
            with Path(spec).open('rt') as inf:
                with Path(self.dist_dir, spec).open('wt') as outf:
                    outf.write(string.Template(inf.read()).substitute(subst))


class build_py(setuptools.command.build_py.build_py):
    def run(self):
        self.run_command('meta')
        super().run()


with Path("README.rst").open("rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name = "photoidx",
    version = version,
    description = docstring.split("\n")[0],
    long_description = readme,
    url = "https://github.com/RKrahl/photoidx",
    author = "Rolf Krahl",
    author_email = "rolf@rotkraut.de",
    license = "Apache-2.0",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages = ["photoidx", "photoidx.qt"],
    scripts = ["scripts/photo-idx.py", "scripts/imageview.py"],
    python_requires = ">=3.6",
    install_requires = ["PyYAML", "ExifRead >= 2.2.0"],
    cmdclass = dict(cmdclass, build_py=build_py, sdist=sdist, meta=meta),
)
