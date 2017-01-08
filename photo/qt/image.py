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

    def getPixmap(self):
        image = QtGui.QImage(self.fileName)
        if image.isNull():
            raise ImageNotFoundError("Cannot load %s." % self.fileName)
        pixmap = QtGui.QPixmap.fromImage(image)
        if self.item.orientation:
            rm = QtGui.QMatrix()
            m = re.match(r"Rotate (\d+) CW", self.item.orientation)
            if m:
                rm = rm.rotate(int(m.group(1)))
            return pixmap.transformed(rm)
        else:
            return pixmap
