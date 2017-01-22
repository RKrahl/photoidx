"""Provide the class Image corresponding to an IdxItem.
"""

import os.path
import re
from PySide import QtCore, QtGui
try:
    import vignette
except ImportError:
    vignette = None

# Disable vignette tumbnailer backends that are not useful in the
# context of photo-tools.
if vignette:
    for backcls in (vignette.OooCliBackend, 
                    vignette.PopplerCliBackend, 
                    vignette.FFMpegCliBackend):
        for i in reversed(range(len(vignette.THUMBNAILER_BACKENDS))):
            if isinstance(vignette.THUMBNAILER_BACKENDS[i], backcls):
                del vignette.THUMBNAILER_BACKENDS[i]


class ImageNotFoundError(Exception):
    pass


class Image(object):

    ThumbnailSize = QtCore.QSize(128, 128)

    def __init__(self, basedir, item):
        self.item = item
        self.fileName = os.path.join(basedir, item.filename)
        self.name = item.name or os.path.basename(self.fileName)
        self.transform = QtGui.QMatrix()
        if self.item.orientation:
            m = re.match(r"Rotate (\d+) CW", self.item.orientation)
            if m:
                self.rotate(int(m.group(1)))

    def getPixmap(self):
        image = QtGui.QImage(self.fileName)
        if image.isNull():
            raise ImageNotFoundError("Cannot load %s." % self.fileName)
        return QtGui.QPixmap.fromImage(image).transformed(self.transform)

    def getThumbPixmap(self):
        if vignette:
            thumbpath = vignette.get_thumbnail(self.fileName, 'normal')
            image = QtGui.QImage(thumbpath)
            if image.isNull():
                raise ImageNotFoundError("Cannot load %s." % self.fileName)
            pixmap = QtGui.QPixmap.fromImage(image)
        else:
            image = QtGui.QImage(self.fileName)
            if image.isNull():
                raise ImageNotFoundError("Cannot load %s." % self.fileName)
            pixmap = QtGui.QPixmap.fromImage(image)
            pixmap = pixmap.scaled(self.ThumbnailSize, 
                                   QtCore.Qt.KeepAspectRatio, 
                                   QtCore.Qt.SmoothTransformation)
        pixmap = pixmap.transformed(self.transform)
        return pixmap

    def rotate(self, a):
        self.transform.rotate(a)
