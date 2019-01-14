"""Provide a PySide ImageViewer window.
"""

import sys
from PySide import QtCore, QtGui
import photo.index
from photo.listtools import LazyList
from photo.qt.image import Image
from photo.qt.filterDialog import FilterDialog
from photo.qt.imageInfoDialog import ImageInfoDialog
from photo.qt.overviewWindow import OverviewWindow
from photo.qt.tagSelectDialog import TagSelectDialog


class ImageViewer(QtGui.QMainWindow):

    def __init__(self, images, imgFilter, 
                 scaleFactor=1.0, readOnly=False, dirty=False):
        super().__init__()

        self.images = images
        self.imgFilter = imgFilter
        self.selection = LazyList(self._filteredImages())
        self.scaleFactor = scaleFactor
        self.readOnly = readOnly
        self.dirty = dirty
        self.cur = 0

        self.imageInfoDialog = ImageInfoDialog(self.images.directory)
        self.overviewwindow = None

        if not self.readOnly:
            taglist = set()
            for i in images:
                taglist |= i.tags
            self.tagSelectDialog = TagSelectDialog(taglist)
        else:
            self.tagSelectDialog = None

        self.filterDialog = FilterDialog()

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

        self.saveAct = QtGui.QAction("&Save index", self, 
                shortcut="Ctrl+s", enabled=(not self.readOnly), 
                triggered=self.saveIndex)
        self.closeAct = QtGui.QAction("&Close", self, 
                shortcut="q", triggered=self.close)
        self.filterOptsAct = QtGui.QAction("Filter Options", self,
                shortcut="Shift+Ctrl+f", triggered=self.filterOptions)
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
        self.overviewAct = QtGui.QAction("&Overview Window", self,
                shortcut="o", triggered=self.overview)
        self.prevImageAct = QtGui.QAction("&Previous Image", self,
                shortcut="p", enabled=False, triggered=self.prevImage)
        self.nextImageAct = QtGui.QAction("&Next Image", self,
                shortcut="n", enabled=(self._haveNext()), 
                triggered=self.nextImage)
        self.selectImageAct = QtGui.QAction("&Select Image", self,
                shortcut="s", enabled=(not self.readOnly), 
                triggered=self.selectImage)
        self.deselectImageAct = QtGui.QAction("&Deselect Image", self,
                shortcut="d", enabled=(not self.readOnly), 
                triggered=self.deselectImage)
        self.pushForwardAct = QtGui.QAction("Push Image &Forward", self,
                shortcut="Ctrl+f", enabled=(not self.readOnly), 
                triggered=self.pushImageForward)
        self.pushBackwardAct = QtGui.QAction("Push Image &Backward", self,
                shortcut="Ctrl+b", enabled=(not self.readOnly), 
                triggered=self.pushImageBackward)
        self.tagSelectAct = QtGui.QAction("&Tags", self,
                shortcut="t", enabled=(not self.readOnly), 
                triggered=self.tagSelect)

        self.fileMenu = QtGui.QMenu("&File", self)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.closeAct)
        self.fileMenu.addAction(self.filterOptsAct)
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
        self.viewMenu.addAction(self.overviewAct)
        self.menuBar().addMenu(self.viewMenu)

        self.imageMenu = QtGui.QMenu("&Image", self)
        self.imageMenu.addAction(self.prevImageAct)
        self.imageMenu.addAction(self.nextImageAct)
        self.imageMenu.addAction(self.selectImageAct)
        self.imageMenu.addAction(self.deselectImageAct)
        self.imageMenu.addSeparator()
        self.imageMenu.addAction(self.pushForwardAct)
        self.imageMenu.addAction(self.pushBackwardAct)
        self.imageMenu.addSeparator()
        self.imageMenu.addAction(self.tagSelectAct)
        self.menuBar().addMenu(self.imageMenu)

        self.show()
        self._extraSize = self.size() - self.scrollArea.viewport().size()
        self._loadImage()
        self._checkActions()

    def saveIndex(self):
        self.images.write()
        self.dirty = False

    def close(self):
        if self.overviewwindow:
            self.overviewwindow.close()
        super().close()

    def _filteredImages(self):
        for item in self.images:
            if self.imgFilter(item):
                yield Image(self.images.directory, item)

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
        maxSize = self.maximumSize()
        imgSize = self.imageLabel.pixmap().size()
        if self.scaleFactor is None:
            size = maxSize - self._extraSize
            hscale = size.width() / imgSize.width()
            vscale = size.height() / imgSize.height()
            self.scaleFactor = min(hscale, vscale)
        size = self.scaleFactor * imgSize
        winSize = size + self._extraSize
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
            image = self.selection[self.cur]
        except IndexError:
            # Nothing to view.
            self.imageLabel.hide()
            if self.overviewwindow:
                self.overviewwindow.markActive(None)
            return
        try:
            pixmap = image.getPixmap()
        except Exception as e:
            print(str(e), file=sys.stderr)
            del self.selection[self.cur]
            if self.overviewwindow:
                self.overviewwindow.updateThumbs()
            self._loadImage()
            return
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.show()
        self._setSize()
        self.setWindowTitle(image.name)
        if self.overviewwindow:
            self.overviewwindow.markActive(image)

    def _checkActions(self):
        """Enable and disable actions as appropriate.
        """
        self.prevImageAct.setEnabled(self.cur > 0)
        self.pushForwardAct.setEnabled(not self.readOnly and self.cur > 0)
        self.nextImageAct.setEnabled(self._haveNext())
        self.pushBackwardAct.setEnabled(not self.readOnly and self._haveNext())
        try:
            item = self.selection[self.cur].item
        except IndexError:
            # No current image.
            self.imageInfoAct.setEnabled(False)
            self.selectImageAct.setEnabled(False)
            self.deselectImageAct.setEnabled(False)
            self.tagSelectAct.setEnabled(False)
            self.zoomInAct.setEnabled(False)
            self.zoomOutAct.setEnabled(False)
            self.zoomFitHeightAct.setEnabled(False)
            self.zoomFitWidthAct.setEnabled(False)
            self.rotateLeftAct.setEnabled(False)
            self.rotateRightAct.setEnabled(False)
        else:
            self.imageInfoAct.setEnabled(True)
            en_select = not self.readOnly and not item.selected
            en_deselect = not self.readOnly and item.selected
            self.selectImageAct.setEnabled(en_select)
            self.deselectImageAct.setEnabled(en_deselect)
            self.tagSelectAct.setEnabled(not self.readOnly)
            self.zoomInAct.setEnabled(True)
            self.zoomOutAct.setEnabled(True)
            self.zoomFitHeightAct.setEnabled(True)
            self.zoomFitWidthAct.setEnabled(True)
            self.rotateLeftAct.setEnabled(True)
            self.rotateRightAct.setEnabled(True)

    def _reevalFilter(self):
        """Re-evaluate the filter on the current image.
        This is needed if relevant attributes have changed.
        """
        if not self.imgFilter(self.selection[self.cur].item):
            del self.selection[self.cur]
            if self.overviewwindow:
                self.overviewwindow.updateThumbs()
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
        image = self.selection[self.cur]
        image.rotate(-90)
        self.imageLabel.setPixmap(image.getPixmap())
        self._setSize()
        if self.overviewwindow:
            w = self.overviewwindow.getThumbnailWidget(image)
            if w:
                w.setImagePixmap()

    def rotateRight(self):
        image = self.selection[self.cur]
        image.rotate(90)
        self.imageLabel.setPixmap(image.getPixmap())
        self._setSize()
        if self.overviewwindow:
            w = self.overviewwindow.getThumbnailWidget(image)
            if w:
                w.setImagePixmap()

    def fullScreen(self):
        if self.fullScreenAct.isChecked():
            self.showFullScreen()
        else:
            self.showNormal()
            self._setSize()

    def moveCurrentTo(self, newcur):
        if isinstance(newcur, Image):
            newcur = self.selection.index(newcur)
        self.cur = newcur
        self._loadImage()
        self._setSize()
        self._checkActions()

    def prevImage(self):
        if self.cur > 0:
            self.moveCurrentTo(self.cur - 1)

    def nextImage(self):
        if self._haveNext():
            self.moveCurrentTo(self.cur + 1)

    def selectImage(self):
        try:
            self.selection[self.cur].item.selected = True
        except IndexError:
            # No current image.
            pass
        else:
            self.dirty = True
            self.selectImageAct.setEnabled(False)
            self.deselectImageAct.setEnabled(True)
            self._reevalFilter()

    def deselectImage(self):
        try:
            self.selection[self.cur].item.selected = False
        except IndexError:
            # No current image.
            pass
        else:
            self.dirty = True
            self.selectImageAct.setEnabled(True)
            self.deselectImageAct.setEnabled(False)
            self._reevalFilter()

    def imageInfo(self):
        self.imageInfoDialog.setinfo(self.selection[self.cur].item)
        self.imageInfoDialog.exec_()

    def overview(self):
        if not self.overviewwindow:
            self.overviewwindow = OverviewWindow(self)
        self.overviewwindow.show()

    def tagSelect(self):
        item = self.selection[self.cur].item
        self.tagSelectDialog.setCheckedTags(item.tags)
        if self.tagSelectDialog.exec_():
            item.tags = self.tagSelectDialog.checkedTags()
            self.dirty = True
            self._reevalFilter()

    def filterOptions(self):
        self.filterDialog.setfilter(self.imgFilter)
        if self.filterDialog.exec_():
            if self.overviewwindow:
                # The overview window would need to be rebuild in any case.
                self.overviewwindow.close()
                self.overviewwindow = None
            try:
                curidx = self.images.index(self.selection[self.cur].item)
            except IndexError:
                curidx = None
            self.imgFilter = self.filterDialog.imgFilter
            self.selection = LazyList(self._filteredImages())
            if curidx:
                item_i = 0
                for img_i, img in enumerate(self.selection):
                    item_i = self.images.index(img.item, item_i)
                    if item_i >= curidx:
                        cur = img_i
                        break
                else:
                    cur = len(self.selection)
            else:
                cur = 0
            self.moveCurrentTo(cur)

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self._setSize()

    def pushImageForward(self):
        """Move the current image forward one position in the image order.
        """
        if self.cur > 0:
            i = self.images.index(self.selection[self.cur].item)
            pi = self.images.index(self.selection[self.cur - 1].item)
            item = self.images.pop(i)
            self.images.insert(pi, item)
            img = self.selection.pop(self.cur)
            self.selection.insert(self.cur - 1, img)
            self.dirty = True
            if self.overviewwindow:
                self.overviewwindow.updateThumbs()
            self.moveCurrentTo(self.cur - 1)

    def pushImageBackward(self):
        """Move the current image backward one position in the image order.
        """
        if self._haveNext():
            i = self.images.index(self.selection[self.cur].item)
            ni = self.images.index(self.selection[self.cur + 1].item)
            item = self.images.pop(i)
            self.images.insert(ni - 1, item)
            img = self.selection.pop(self.cur)
            self.selection.insert(self.cur + 1, img)
            self.dirty = True
            if self.overviewwindow:
                self.overviewwindow.updateThumbs()
            self.moveCurrentTo(self.cur + 1)
