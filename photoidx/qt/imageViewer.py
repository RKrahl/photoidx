"""Provide a PySide ImageViewer window.
"""

import sys
from PySide2 import QtCore, QtGui, QtWidgets
import photoidx.index
from photoidx.listtools import LazyList
from photoidx.qt.image import Image
from photoidx.qt.filterDialog import FilterDialog
from photoidx.qt.imageInfoDialog import ImageInfoDialog
from photoidx.qt.overviewWindow import OverviewWindow
from photoidx.qt.tagSelectDialog import TagSelectDialog


class ImageViewer(QtWidgets.QMainWindow):

    def __init__(self, images, imgFilter, 
                 scaleFactor=1.0, readOnly=False, dirty=False):
        super().__init__()

        self.images = images
        self.imgFilter = imgFilter
        self.selection = LazyList(self._filteredImages())
        if readOnly:
            dirty = False
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

        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setSizePolicy(QtWidgets.QSizePolicy.Ignored,
                                      QtWidgets.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.setCentralWidget(self.scrollArea)

        maxSize = 0.95 * QtWidgets.QApplication.desktop().screenGeometry().size()
        self.setMaximumSize(maxSize)

        self.saveAct = QtWidgets.QAction("&Save index", self)
        self.saveAct.setShortcut("Ctrl+s")
        self.saveAct.setEnabled(not self.readOnly)
        self.saveAct.triggered.connect(self.saveIndex)
        self.closeAct = QtWidgets.QAction("&Close", self)
        self.closeAct.setShortcut("q")
        self.closeAct.triggered.connect(self.close)
        self.filterOptsAct = QtWidgets.QAction("Filter Options", self)
        self.filterOptsAct.setShortcut("Shift+Ctrl+f")
        self.filterOptsAct.triggered.connect(self.filterOptions)
        self.zoomInAct = QtWidgets.QAction("Zoom &In", self)
        self.zoomInAct.setShortcut(">")
        self.zoomInAct.triggered.connect(self.zoomIn)
        self.zoomOutAct = QtWidgets.QAction("Zoom &Out", self)
        self.zoomOutAct.setShortcut("<")
        self.zoomOutAct.triggered.connect(self.zoomOut)
        self.zoomFitHeightAct = QtWidgets.QAction("Zoom to Fit &Height", self)
        self.zoomFitHeightAct.triggered.connect(self.zoomFitHeight)
        self.zoomFitWidthAct = QtWidgets.QAction("Zoom to Fit &Width", self)
        self.zoomFitWidthAct.triggered.connect(self.zoomFitWidth)
        self.rotateLeftAct = QtWidgets.QAction("Rotate &Left", self)
        self.rotateLeftAct.setShortcut("l")
        self.rotateLeftAct.triggered.connect(self.rotateLeft)
        self.rotateRightAct = QtWidgets.QAction("Rotate &Right", self)
        self.rotateRightAct.setShortcut("r")
        self.rotateRightAct.triggered.connect(self.rotateRight)
        self.fullScreenAct = QtWidgets.QAction("Show &Full Screen", self)
        self.fullScreenAct.setShortcut("f")
        self.fullScreenAct.setCheckable(True)
        self.fullScreenAct.triggered.connect(self.fullScreen)
        self.imageInfoAct = QtWidgets.QAction("Image &Info", self)
        self.imageInfoAct.setShortcut("i")
        self.imageInfoAct.triggered.connect(self.imageInfo)
        self.overviewAct = QtWidgets.QAction("&Overview Window", self)
        self.overviewAct.setShortcut("o")
        self.overviewAct.triggered.connect(self.overview)
        self.prevImageAct = QtWidgets.QAction("&Previous Image", self)
        self.prevImageAct.setShortcut("p")
        self.prevImageAct.setEnabled(False)
        self.prevImageAct.triggered.connect(self.prevImage)
        self.nextImageAct = QtWidgets.QAction("&Next Image", self)
        self.nextImageAct.setShortcut("n")
        self.nextImageAct.setEnabled(self._haveNext())
        self.nextImageAct.triggered.connect(self.nextImage)
        self.selectImageAct = QtWidgets.QAction("&Select Image", self)
        self.selectImageAct.setShortcut("s")
        self.selectImageAct.setEnabled(not self.readOnly)
        self.selectImageAct.triggered.connect(self.selectImage)
        self.deselectImageAct = QtWidgets.QAction("&Deselect Image", self)
        self.deselectImageAct.setShortcut("d")
        self.deselectImageAct.setEnabled(not self.readOnly)
        self.deselectImageAct.triggered.connect(self.deselectImage)
        self.pushForwardAct = QtWidgets.QAction("Push Image &Forward", self)
        self.pushForwardAct.setShortcut("Ctrl+f")
        self.pushForwardAct.setEnabled(not self.readOnly)
        self.pushForwardAct.triggered.connect(self.pushImageForward)
        self.pushBackwardAct = QtWidgets.QAction("Push Image &Backward", self)
        self.pushBackwardAct.setShortcut("Ctrl+b")
        self.pushBackwardAct.setEnabled(not self.readOnly)
        self.pushBackwardAct.triggered.connect(self.pushImageBackward)
        self.tagSelectAct = QtWidgets.QAction("&Tags", self)
        self.tagSelectAct.setShortcut("t")
        self.tagSelectAct.setEnabled(not self.readOnly)
        self.tagSelectAct.triggered.connect(self.tagSelect)

        menu = self.menuBar()

        fileMenu = menu.addMenu("&File")
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.closeAct)
        fileMenu.addAction(self.filterOptsAct)

        viewMenu = menu.addMenu("&View")
        viewMenu.addAction(self.zoomInAct)
        viewMenu.addAction(self.zoomOutAct)
        viewMenu.addAction(self.zoomFitHeightAct)
        viewMenu.addAction(self.zoomFitWidthAct)
        viewMenu.addAction(self.rotateLeftAct)
        viewMenu.addAction(self.rotateRightAct)
        viewMenu.addSeparator()
        viewMenu.addAction(self.fullScreenAct)
        viewMenu.addSeparator()
        viewMenu.addAction(self.imageInfoAct)
        viewMenu.addAction(self.overviewAct)

        imageMenu = menu.addMenu("&Image")
        imageMenu.addAction(self.prevImageAct)
        imageMenu.addAction(self.nextImageAct)
        imageMenu.addAction(self.selectImageAct)
        imageMenu.addAction(self.deselectImageAct)
        imageMenu.addSeparator()
        imageMenu.addAction(self.pushForwardAct)
        imageMenu.addAction(self.pushBackwardAct)
        imageMenu.addSeparator()
        imageMenu.addAction(self.tagSelectAct)

        self.show()
        self._extraSize = self.size() - self.scrollArea.viewport().size()
        self._loadImage()
        self._checkActions()

    def saveIndex(self):
        try:
            self.images.write()
            self.dirty = False
        except photoidx.index.AlreadyLockedError:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Index is locked")
            msgBox.setText("Saving the image index failed!")
            msgBox.setInformativeText("Another process is currently "
                                      "accessing the file")
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.exec_()

    def close(self):
        if self.dirty:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Save index?")
            msgBox.setText("The image index been modified.")
            msgBox.setInformativeText("Save changes before closing?")
            msgBox.setIcon(QtWidgets.QMessageBox.Question)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Save |
                                      QtWidgets.QMessageBox.Discard |
                                      QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == QtWidgets.QMessageBox.Save:
                self.saveIndex()
                if self.dirty:
                    return
            elif ret == QtWidgets.QMessageBox.Discard:
                pass
            elif ret == QtWidgets.QMessageBox.Cancel:
                return
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

    def get_visible_center(self):
        """Get the center of the current visible area in image coordinates.
        """
        hscroll_pos = self.scrollArea.horizontalScrollBar().value()
        vscroll_pos = self.scrollArea.verticalScrollBar().value()
        scroll_pos = QtCore.QSize(hscroll_pos, vscroll_pos)
        win_center = scroll_pos + self.scrollArea.viewport().size() / 2
        return win_center / self.scaleFactor

    def scroll_visible_center_to(self, pos):
        """Move the scrollbars to center the position in the visible area.
        """
        win_center = self.scaleFactor * pos
        scroll_pos = win_center - self.scrollArea.viewport().size() / 2
        self.scrollArea.horizontalScrollBar().setValue(scroll_pos.width())
        self.scrollArea.verticalScrollBar().setValue(scroll_pos.height())

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
        center = self.get_visible_center()
        self.scaleFactor *= factor
        self._setSize()
        self.scroll_visible_center_to(center)

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
