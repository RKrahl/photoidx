"""Provide the class Image corresponding to an IdxItem.
"""

import logging
import re
from PySide2 import QtCore, QtGui, QtWidgets
try:
    import vignette
except ImportError:
    vignette = None

log = logging.getLogger(__name__)

# Limit the vignette thumbnailer backends to those dealing with images.
if vignette:
    try:
        # vignette 4.5.2 or newer
        vignette.select_thumbnailer_types([vignette.FILETYPE_IMAGE])
    except AttributeError:
        if hasattr(vignette, 'THUMBNAILER_BACKENDS'):
            # vignette 4.3.0 or newer
            vignette.THUMBNAILER_BACKENDS = [
                vignette.QtBackend(),
                vignette.PilBackend(),
                vignette.MagickBackend()
            ]
        else:
            # vignette is too old to be usable
            vignette = None
    if vignette:
        if not list(vignette.iter_thumbnail_backends()):
            log.warning("Disabling vignette: "
                        "no suitable thumbnailer backend available")
            vignette = None


class ImageNotFoundError(Exception):
    pass


class Image(object):

    ThumbnailSize = QtCore.QSize(128, 128)

    def __init__(self, basedir, item):
        self.item = item
        self.fileName = basedir / item.filename
        self.name = item.name or self.fileName.name
        self.transform = QtGui.QMatrix()
        if self.item.orientation:
            m = re.match(r"Rotate (\d+) CW", self.item.orientation)
            if m:
                self.rotate(int(m.group(1)))

    def getPixmap(self):
        image = QtGui.QImage(str(self.fileName))
        if image.isNull():
            raise ImageNotFoundError("Cannot load %s." % self.fileName)
        return QtGui.QPixmap.fromImage(image).transformed(self.transform)

    def getThumbPixmap(self):
        if vignette:
            thumbpath = vignette.get_thumbnail(str(self.fileName), 'normal')
            image = QtGui.QImage(thumbpath)
            if image.isNull():
                raise ImageNotFoundError("Cannot load %s." % self.fileName)
            pixmap = QtGui.QPixmap.fromImage(image)
        else:
            image = QtGui.QImage(str(self.fileName))
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
