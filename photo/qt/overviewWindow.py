"""An overview window showing thumbnails of the image set.
"""

from __future__ import division
import math
from PySide import QtCore, QtGui


class ThumbnailWidget(QtGui.QLabel):

    def __init__(self, image, scale):
        super(ThumbnailWidget, self).__init__()
        pixmap = image.getPixmap()
        size = scale * pixmap.size()
        pixmap = pixmap.scaled(size)
        self.setPixmap(pixmap)


class OverviewWindow(QtGui.QMainWindow):

    def __init__(self, imageViewer):
        super(OverviewWindow, self).__init__()

        self.imageViewer = imageViewer
        self.numcolumns = 4
        self.scaleFactor = self.imageViewer.scaleFactor / 5.0

        self.setWindowTitle("Overview")
        self.mainLayout = QtGui.QGridLayout()
        self._populate()

        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(self.mainLayout)
        scrollArea = QtGui.QScrollArea()
        scrollArea.setWidget(centralWidget)
        scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.setCentralWidget(scrollArea)

    def _populate(self):
        """Populate the mainLayout with thumbnail images.
        """
        # FIXME: by now, implement only the initial setup of the image
        # list.  Must also support updating the list after changes in
        # imageViewer.selection.
        images = self.imageViewer.selection
        ncol = self.numcolumns
        c = 0
        for i in images:
            thumb = ThumbnailWidget(i, self.scaleFactor)
            self.mainLayout.addWidget(thumb, c // ncol, c % ncol)
            c += 1
