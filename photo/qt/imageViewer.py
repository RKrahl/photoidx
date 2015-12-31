"""Provide a PySide ImageViewer window.
"""

from __future__ import division
import os.path
import re
from PySide import QtCore, QtGui


class ImageViewer(QtGui.QMainWindow):

    def __init__(self, images, taglist=None, date=None, filelist=None, 
                 scaleFactor=1.0):
        super(ImageViewer, self).__init__()

        self.images = images
        self.taglist = taglist
        self.date = date
        self.filelist = filelist
        self.scaleFactor = scaleFactor
        self.selection = list(images.filtered(taglist, date, filelist))

        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored,
                                      QtGui.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.setCentralWidget(self.scrollArea)

        maxSize = 0.95 * QtGui.QApplication.desktop().screenGeometry().size()
        self.setMaximumSize(maxSize)

        self.closeAct = QtGui.QAction("&Close", self, 
                shortcut="q", triggered=self.close)
        self.zoomInAct = QtGui.QAction("Zoom &In", self,
                shortcut=">", triggered=self.zoomIn)
        self.zoomOutAct = QtGui.QAction("Zoom &Out", self,
                shortcut="<", triggered=self.zoomOut)
        self.zoomFitHeightAct = QtGui.QAction("Zoom to Fit &Height", self,
                triggered=self.zoomFitHeight)
        self.zoomFitWidthAct = QtGui.QAction("Zoom to Fit &Width", self,
                triggered=self.zoomFitWidth)
        self.rotateLeftAct = QtGui.QAction("Rotate &Left", self,
                shortcut="l", triggered=self.rotateLeft)
        self.rotateRightAct = QtGui.QAction("Rotate &Right", self,
                shortcut="r", triggered=self.rotateRight)
        self.fullScreenAct = QtGui.QAction("Show &Full Screen", self,
                shortcut="f", checkable=True, triggered=self.fullScreen)
        self.prevImageAct = QtGui.QAction("&Previous Image", self,
                shortcut="p", enabled=False, triggered=self.prevImage)
        self.nextImageAct = QtGui.QAction("&Next Image", self,
                shortcut="n", enabled=(len(self.selection)>1), 
                triggered=self.nextImage)

        self.fileMenu = QtGui.QMenu("&File", self)
        self.fileMenu.addAction(self.closeAct)
        self.menuBar().addMenu(self.fileMenu)

        self.viewMenu = QtGui.QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.zoomFitHeightAct)
        self.viewMenu.addAction(self.zoomFitWidthAct)
        self.viewMenu.addAction(self.rotateLeftAct)
        self.viewMenu.addAction(self.rotateRightAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fullScreenAct)
        self.menuBar().addMenu(self.viewMenu)

        self.imageMenu = QtGui.QMenu("&Image", self)
        self.imageMenu.addAction(self.prevImageAct)
        self.imageMenu.addAction(self.nextImageAct)
        self.menuBar().addMenu(self.imageMenu)

        self.cur = 0
        if not self.selection:
            raise RuntimeError("Nothing to view.")
        self.loadImage(self.selection[self.cur])
        self.show()
        self._extraSize = self.size() - self.scrollArea.viewport().size()
        self._setSize()

    def _setSize(self):
        size = self.scaleFactor * self.imageLabel.pixmap().size()
        winSize = size + self._extraSize
        maxSize = self.maximumSize()
        if winSize.height() > maxSize.height():
            # Take vertical scrollbar into account.
            sbw = self.scrollArea.verticalScrollBar().size().width()
            winSize += QtCore.QSize(sbw, 0)
        if winSize.width() > maxSize.width():
            # Take horizontal scrollbar into account.
            sbh = self.scrollArea.horizontalScrollBar().size().height()
            winSize += QtCore.QSize(0, sbh)
        self.imageLabel.resize(size)
        if not self.fullScreenAct.isChecked():
            self.resize(winSize)

    def loadImage(self, item):
        fileName = item.filename
        image = QtGui.QImage(fileName)
        if image.isNull():
            raise RuntimeError("Cannot load %s." % fileName)
        pixmap = QtGui.QPixmap.fromImage(image)
        rm = QtGui.QMatrix()
        if item.orientation:
            m = re.match(r"Rotate (\d+) CW", item.orientation)
            if m:
                rm = rm.rotate(int(m.group(1)))
        self.imageLabel.setPixmap(pixmap.transformed(rm))
        self.setWindowTitle(os.path.basename(fileName))

    def zoomIn(self):
        self.scaleImage(1.6)

    def zoomOut(self):
        self.scaleImage(0.625)

    def zoomFitHeight(self):
        imgHeight = self.imageLabel.pixmap().size().height()
        winHeight = self.scrollArea.viewport().size().height()
        # Leave an internal padding of a few pixel
        winHeight -= 6
        self.scaleFactor = winHeight / imgHeight
        self._setSize()

    def zoomFitWidth(self):
        imgWidth = self.imageLabel.pixmap().size().width()
        winWidth = self.scrollArea.viewport().size().width()
        # Leave an internal padding of a few pixel
        winWidth -= 6
        self.scaleFactor = winWidth / imgWidth
        self._setSize()

    def rotateLeft(self):
        rm = QtGui.QMatrix().rotate(-90)
        self.imageLabel.setPixmap(self.imageLabel.pixmap().transformed(rm))
        self._setSize()

    def rotateRight(self):
        rm = QtGui.QMatrix().rotate(90)
        self.imageLabel.setPixmap(self.imageLabel.pixmap().transformed(rm))
        self._setSize()

    def fullScreen(self):
        if self.fullScreenAct.isChecked():
            self.showFullScreen()
        else:
            self.showNormal()
            self._setSize()

    def prevImage(self):
        if self.cur > 0:
            self.cur -= 1
            self.loadImage(self.selection[self.cur])
            self._setSize()
            self.nextImageAct.setEnabled(True)
        self.prevImageAct.setEnabled(self.cur > 0)

    def nextImage(self):
        if self.cur < len(self.selection)-1:
            self.cur += 1
            self.loadImage(self.selection[self.cur])
            self._setSize()
            self.prevImageAct.setEnabled(True)
        self.nextImageAct.setEnabled(self.cur < len(self.selection)-1)

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self._setSize()
