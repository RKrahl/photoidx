"""An overview window showing thumbnails of the image set.
"""

import sys
import math
from PySide2 import QtCore, QtWidgets


class ThumbnailWidget(QtWidgets.QLabel):

    def __init__(self, image):
        super().__init__()

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


class OverviewWindow(QtWidgets.QMainWindow):

    def __init__(self, imageViewer):
        super().__init__()

        self.imageViewer = imageViewer
        self.numcolumns = 4

        self.setWindowTitle("Overview")
        self.mainLayout = QtWidgets.QGridLayout()
        self._populate()

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(self.mainLayout)
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidget(centralWidget)
        scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.setCentralWidget(scrollArea)

        self.closeAct = QtWidgets.QAction("&Close", self)
        self.closeAct.triggered.connect(self.close)

        menu = self.menuBar()

        self.fileMenu = menu.addMenu("&File")
        self.fileMenu.addAction(self.closeAct)

        # Set the width of the window such that the scrollArea just
        # fits.  We need to add 24 to the central widget, 20 for the
        # vertical scroll bar and 4 for the border.
        width = centralWidget.size().width() + 24
        size = self.size()
        size.setWidth(width)
        self.resize(size)

        self.activeWidget = None
        try:
            image = self.imageViewer.selection[self.imageViewer.cur]
            self.markActive(image)
        except IndexError:
            pass

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
