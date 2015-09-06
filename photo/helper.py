"""A collection of internal helpers.

**Note**: This module is intended for the internal use in the photo
package and is not considered to be part of the API.
"""

import os


class tmpchdir:
    """Temporarily change the current working directory.
    """
    def __init__(self, path):
        self.savewd = os.getcwd()
        self.wd = path
    def __enter__(self):
        os.chdir(self.wd)
        return self.wd
    def __exit__(self, type, value, tb):
        os.chdir(self.savewd)

