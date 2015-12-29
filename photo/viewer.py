"""Provide a PySide ImageViewer window.
"""

import os.path
from PySide import QtCore, QtGui


class ImageViewer(QtGui.QMainWindow):

    def __init__(self, fileNames, scaleFactor=1.0):
        super(ImageViewer, self).__init__()

        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored,
                                      QtGui.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.scrollArea)

        self.fileNames = fileNames
        self.scaleFactor = scaleFactor
        maxSize = 0.9 * QtGui.QApplication.desktop().screenGeometry().size()
        self.setMaximumSize(maxSize)

        self.closeAct = QtGui.QAction("&Close", self, shortcut="W",
                triggered=self.close)
        self.zoomInAct = QtGui.QAction("Zoom &In", self,
                shortcut=">", triggered=self.zoomIn)
        self.zoomOutAct = QtGui.QAction("Zoom &Out", self,
                shortcut="<", triggered=self.zoomOut)
        self.rotateLeftAct = QtGui.QAction("Rotate &Left", self,
                shortcut="l", triggered=self.rotateLeft)
        self.rotateRightAct = QtGui.QAction("Rotate &Right", self,
                shortcut="r", triggered=self.rotateRight)
        self.prevImageAct = QtGui.QAction("&Previous Image", self,
                shortcut="p", enabled=False, triggered=self.prevImage)
        self.nextImageAct = QtGui.QAction("&Next Image", self,
                shortcut="n", enabled=(len(self.fileNames)>1), 
                triggered=self.nextImage)

        self.fileMenu = QtGui.QMenu("&File", self)
        self.fileMenu.addAction(self.closeAct)
        self.menuBar().addMenu(self.fileMenu)

        self.viewMenu = QtGui.QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.rotateLeftAct)
        self.viewMenu.addAction(self.rotateRightAct)
        self.menuBar().addMenu(self.viewMenu)

        self.imageMenu = QtGui.QMenu("&Image", self)
        self.imageMenu.addAction(self.prevImageAct)
        self.imageMenu.addAction(self.nextImageAct)
        self.menuBar().addMenu(self.imageMenu)

        self.cur = 0
        self.loadImage(self.fileNames[self.cur])
        self.show()
        self._extraSize = self.size() - self.scrollArea.viewport().size()
        self._setSize()

    def _setSize(self):
        size = self.scaleFactor * self.imageLabel.pixmap().size()
        self.imageLabel.resize(size)
        self.resize(size + self._extraSize)

    def loadImage(self, fileName):
        image = QtGui.QImage(fileName)
        if image.isNull():
            raise RuntimeError("Cannot load %s." % fileName)
        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
        self.setWindowTitle(os.path.basename(fileName))

    def zoomIn(self):
        self.scaleImage(1.6)

    def zoomOut(self):
        self.scaleImage(0.625)

    def rotateLeft(self):
        rm = QtGui.QMatrix().rotate(-90)
        self.imageLabel.setPixmap(self.imageLabel.pixmap().transformed(rm))
        self._setSize()

    def rotateRight(self):
        rm = QtGui.QMatrix().rotate(90)
        self.imageLabel.setPixmap(self.imageLabel.pixmap().transformed(rm))
        self._setSize()

    def prevImage(self):
        if self.cur > 0:
            self.cur -= 1
            self.loadImage(self.fileNames[self.cur])
            self._setSize()
            self.nextImageAct.setEnabled(True)
        self.prevImageAct.setEnabled(self.cur > 0)

    def nextImage(self):
        if self.cur < len(self.fileNames)-1:
            self.cur += 1
            self.loadImage(self.fileNames[self.cur])
            self._setSize()
            self.prevImageAct.setEnabled(True)
        self.nextImageAct.setEnabled(self.cur < len(self.fileNames)-1)

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self._setSize()
