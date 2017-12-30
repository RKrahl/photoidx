#! /usr/bin/python

import sys
import argparse
from PySide import QtGui
import photo.index
import photo.idxfilter
from photo.qt import ImageViewer


argparser = argparse.ArgumentParser()
argparser.add_argument('-d', '--directory', help="image directory", default=".")
argparser.add_argument('--scale', help="scale factor")
photo.idxfilter.addFilterArguments(argparser)
args = argparser.parse_args()

app = QtGui.QApplication([])
try:
    idx = photo.index.Index(idxfile=args.directory)
    tagSelect=True
except IOError:
    idx = photo.index.Index(imgdir=args.directory)
    tagSelect=False
idxfilter = photo.idxfilter.IdxFilter(args)
imageViewer = ImageViewer(idx, idxfilter, args.scale, tagSelect)
sys.exit(app.exec_())
