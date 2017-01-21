"""An overview window showing thumbnails of the image set.
"""

from __future__ import division, print_function
import sys
import math
from PySide import QtCore, QtGui


class ThumbnailWidget(QtGui.QLabel):

    def __init__(self, image):
        super(ThumbnailWidget, self).__init__()

        self.setFrameStyle(self.Box | self.Plain)
        self.setLineWidth(4)
        palette = self.palette()
        frameColor = palette.color(self.backgroundRole())
        palette.setColor(self.foregroundRole(), frameColor)
        self.setPalette(palette)

        self.image = image
        self.setImagePixmap()

    def _getOverviewWindow(self):
        w = self
        while not isinstance(w, OverviewWindow):
            w = w.parent()
        return w

    def setImagePixmap(self):
        self.setPixmap(self.image.getThumbPixmap())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            ovwin = self._getOverviewWindow()
            ovwin.imageViewer.moveCurrentTo(self.image)

    def markActive(self, isActive):
        palette = self.palette()
        if isActive:
            frameColor = QtCore.Qt.blue
        else:
            frameColor = palette.color(self.backgroundRole())
        palette.setColor(self.foregroundRole(), frameColor)
        self.setPalette(palette)


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

        self.activeWidget = None
        self.markActive(self.imageViewer.selection[self.imageViewer.cur])

    def _populate(self):
        """Populate the mainLayout with thumbnail images.
        """
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

    def updateThumbs(self):
        """Update the mainLayout with thumbnail images.
        """
        # Note: this code is based on the assumption that no image
        # will ever be added to self.imageViewer.selection and thus we
        # only need to consider removing ThumbnailWidgets, but not to
        # add any.  Furthermore, we assume the order given by
        # self.mainLayout.itemAt() is the the order that the widgets
        # have been added to self.mainLayout and thus the same as
        # self.imageViewer.selection.
        numImages = len(self.imageViewer.selection)
        for i in range(numImages):
            widget = self.mainLayout.itemAt(i).widget()
            image = self.imageViewer.selection[i]
            if widget.image is not image:
                widget.image = image
                widget.setImagePixmap()
        while self.mainLayout.count() > numImages:
            item = self.mainLayout.takeAt(numImages)
            item.widget().deleteLater()

    def getThumbnailWidget(self, image):
        for i in range(self.mainLayout.count()):
            w = self.mainLayout.itemAt(i).widget()
            if w.image is image:
                return w
        else:
            return None

    def markActive(self, image):
        if self.activeWidget:
            self.activeWidget.markActive(False)
        self.activeWidget = self.getThumbnailWidget(image)
        if self.activeWidget:
            self.activeWidget.markActive(True)
