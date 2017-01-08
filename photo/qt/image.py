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
        rm = None
        try:
            rm = self.item.rotmatrix
        except AttributeError:
            if self.item.orientation:
                m = re.match(r"Rotate (\d+) CW", self.item.orientation)
                if m:
                    rm = QtGui.QMatrix().rotate(int(m.group(1)))
                    self.item.rotmatrix = rm
        if rm:
            return pixmap.transformed(rm)
        else:
            return pixmap
