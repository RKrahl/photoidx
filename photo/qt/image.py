"""Provide the class Image corresponding to an IdxItem.
"""

import os.path
import re
from PySide import QtGui


class ImageNotFoundError(Exception):
    pass


class Image(object):

    def __init__(self, basedir, item):
        self.item = item
        self.fileName = os.path.join(basedir, item.filename)
        self.name = item.name or os.path.basename(self.fileName)
        self.transform = QtGui.QMatrix()
        if self.item.orientation:
            m = re.match(r"Rotate (\d+) CW", self.item.orientation)
            if m:
                self.transform.rotate(int(m.group(1)))

    def getPixmap(self):
        image = QtGui.QImage(self.fileName)
        if image.isNull():
            raise ImageNotFoundError("Cannot load %s." % self.fileName)
        return QtGui.QPixmap.fromImage(image).transformed(self.transform)
