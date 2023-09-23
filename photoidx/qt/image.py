"""Provide the class Image corresponding to an IdxItem.
"""

import logging
import re
from packaging.version import Version
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

_thumbs_oriented = (vignette and
                    Version(vignette.__version__) >= Version('5.0.0'))

class ImageNotFoundError(Exception):
    pass


_OrientationTransform = {
    1: (1, 0, 0, 1),
    2: (-1, 0, 0, 1),
    3: (-1, 0, 0, -1),
    4: (1, 0, 0, -1),
    5: (0, 1, 1, 0),
    6: (0, 1, -1, 0),
    7: (0, -1, -1, 0),
    8: (0, -1, 1, 0),
}
def _get_transform(orientation):
    if orientation is not None:
        return QtGui.QMatrix(*_OrientationTransform[orientation], 0, 0)
    else:
        return QtGui.QMatrix()


class Image(object):

    ThumbnailSize = QtCore.QSize(128, 128)

    def __init__(self, basedir, item):
        self.item = item
        self.fileName = basedir / item.filename
        self.name = item.name or self.fileName.name
        self.init_transform = _get_transform(self.item.orientation)
        self.post_transform = QtGui.QMatrix()

    @property
    def transform(self):
        return self.post_transform * self.init_transform

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
        if _thumbs_oriented:
            transform = self.post_transform
        else:
            transform = self.transform
        pixmap = pixmap.transformed(transform)
        return pixmap

    def rotate(self, a):
        self.post_transform.rotate(a)
