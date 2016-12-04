"""Provide a PySide ImageViewer window.
"""

from __future__ import division, print_function
import sys
import os.path
import re
from PySide import QtCore, QtGui
import photo.index
from photo.listtools import LazyList
from photo.qt.tagSelectDialog import TagSelectDialog
from photo.qt.imageInfoDialog import ImageInfoDialog


class ImageViewer(QtGui.QMainWindow):

    def __init__(self, images, imgFilter, scaleFactor=1.0, tagSelect=True):
        super(ImageViewer, self).__init__()

        self.images = images
        self.imgFilter = imgFilter
        self.selection = LazyList(self.imgFilter.filter(self.images))
        self.scaleFactor = scaleFactor
        self.cur = 0

        self.imageInfoDialog = ImageInfoDialog()

        if tagSelect:
            taglist = set()
            for i in images:
                taglist |= i.tags
            self.tagSelectDialog = TagSelectDialog(taglist)
        else:
            self.tagSelectDialog = None

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
        self.imageInfoAct = QtGui.QAction("Image &Info", self,
                shortcut="i", triggered=self.imageInfo)
        self.prevImageAct = QtGui.QAction("&Previous Image", self,
                shortcut="p", enabled=False, triggered=self.prevImage)
        self.nextImageAct = QtGui.QAction("&Next Image", self,
                shortcut="n", enabled=(self._haveNext()), 
                triggered=self.nextImage)
        self.selectImageAct = QtGui.QAction("&Select Image", self,
                shortcut="s", triggered=self.selectImage)
        self.deselectImageAct = QtGui.QAction("&Deselect Image", self,
                shortcut="d", triggered=self.deselectImage)
        self.tagSelectAct = QtGui.QAction("&Tags", self,
                shortcut="t", enabled=tagSelect, triggered=self.tagSelect)

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
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.imageInfoAct)
        self.menuBar().addMenu(self.viewMenu)

        self.imageMenu = QtGui.QMenu("&Image", self)
        self.imageMenu.addAction(self.prevImageAct)
        self.imageMenu.addAction(self.nextImageAct)
        self.imageMenu.addAction(self.selectImageAct)
        self.imageMenu.addAction(self.deselectImageAct)
        self.imageMenu.addSeparator()
        self.imageMenu.addAction(self.tagSelectAct)
        self.menuBar().addMenu(self.imageMenu)

        self.show()
        self._extraSize = self.size() - self.scrollArea.viewport().size()
        self._loadImage()
        self._checkActions()

    def _haveNext(self):
        """Check whether there is a next image.
        This should be equivalent to self.cur < len(self.selection)-1,
        but without calling len(self.selection).
        """
        try:
            self.selection[self.cur+1]
            return True
        except IndexError:
            return False

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

    def _loadImage(self):
        try:
            item = self.selection[self.cur]
        except IndexError:
            # Nothing to view.
            self.imageLabel.hide()
            return
        fileName = os.path.join(self.images.directory, item.filename)
        title = item.name or os.path.basename(fileName)
        image = QtGui.QImage(fileName)
        if image.isNull():
            print("Cannot load %s." % fileName, file=sys.stderr)
            del self.selection[self.cur]
            self._loadImage()
            return
        pixmap = QtGui.QPixmap.fromImage(image)
        rm = QtGui.QMatrix()
        if item.orientation:
            m = re.match(r"Rotate (\d+) CW", item.orientation)
            if m:
                rm = rm.rotate(int(m.group(1)))
        self.imageLabel.setPixmap(pixmap.transformed(rm))
        self.imageLabel.show()
        self._setSize()
        self.setWindowTitle(title)

    def _checkActions(self):
        """Enable and disable actions as appropriate.
        """
        self.prevImageAct.setEnabled(self.cur > 0)
        self.nextImageAct.setEnabled(self._haveNext())
        try:
            item = self.selection[self.cur]
        except IndexError:
            # No current image.
            self.imageInfoAct.setEnabled(False)
            self.selectImageAct.setEnabled(False)
            self.deselectImageAct.setEnabled(False)
            self.tagSelectAct.setEnabled(False)
        else:
            self.imageInfoAct.setEnabled(True)
            self.selectImageAct.setEnabled(not item.selected)
            self.deselectImageAct.setEnabled(item.selected)
            self.tagSelectAct.setEnabled(self.tagSelectDialog is not None)

    def _reevalFilter(self):
        """Re-evaluate the filter on the current image.
        This is needed if relevant attributes have changed.
        """
        if not self.imgFilter(self.selection[self.cur]):
            del self.selection[self.cur]
            self._loadImage()
            self._checkActions()

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
            self._loadImage()
            self._setSize()
            self._checkActions()

    def nextImage(self):
        if self._haveNext():
            self.cur += 1
            self._loadImage()
            self._setSize()
            self._checkActions()

    def selectImage(self):
        try:
            self.selection[self.cur].selected = True
        except IndexError:
            # No current image.
            pass
        else:
            self.images.write()
            self.selectImageAct.setEnabled(False)
            self.deselectImageAct.setEnabled(True)
            self._reevalFilter()

    def deselectImage(self):
        try:
            self.selection[self.cur].selected = False
        except IndexError:
            # No current image.
            pass
        else:
            self.images.write()
            self.selectImageAct.setEnabled(True)
            self.deselectImageAct.setEnabled(False)
            self._reevalFilter()

    def imageInfo(self):
        self.imageInfoDialog.setinfo(self.selection[self.cur])
        self.imageInfoDialog.exec_()

    def tagSelect(self):
        self.tagSelectDialog.setCheckedTags(self.selection[self.cur].tags)
        if self.tagSelectDialog.exec_():
            self.selection[self.cur].tags = self.tagSelectDialog.checkedTags()
            self.images.write()
            self._reevalFilter()

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self._setSize()
