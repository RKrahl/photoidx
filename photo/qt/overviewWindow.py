"""An overview window showing thumbnails of the image set.
"""

from __future__ import division, print_function
import sys
import math
from PySide import QtCore, QtGui


class ThumbnailWidget(QtGui.QLabel):

    ThumbnailSize = QtCore.QSize(128, 128)

    def __init__(self, image):
        super(ThumbnailWidget, self).__init__()
        self.image = image
        self.setImagePixmap()

    def setImagePixmap(self):
        pixmap = self.image.getPixmap()
        pixmap = pixmap.scaled(self.ThumbnailSize, QtCore.Qt.KeepAspectRatio)
        self.setPixmap(pixmap)


class OverviewWindow(QtGui.QMainWindow):

    def __init__(self, imageViewer):
        super(OverviewWindow, self).__init__()

        self.imageViewer = imageViewer
        self.numcolumns = 4

        self.setWindowTitle("Overview")
        self.mainLayout = QtGui.QGridLayout()
        self._populate()

        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(self.mainLayout)
        scrollArea = QtGui.QScrollArea()
        scrollArea.setWidget(centralWidget)
        scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.setCentralWidget(scrollArea)

        self.closeAct = QtGui.QAction("&Close", self, 
                triggered=self.close)

        self.fileMenu = QtGui.QMenu("&File", self)
        self.fileMenu.addAction(self.closeAct)
        self.menuBar().addMenu(self.fileMenu)

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
            try:
                thumb = ThumbnailWidget(i)
            except Exception as e:
                print(str(e), file=sys.stderr)
            else:
                self.mainLayout.addWidget(thumb, c // ncol, c % ncol,
                                          QtCore.Qt.AlignCenter)
                c += 1

    def getThumbnailWidget(self, image):
        for i in range(self.mainLayout.count()):
            w = self.mainLayout.itemAt(i).widget()
            if w.image is image:
                return w
        else:
            return None
