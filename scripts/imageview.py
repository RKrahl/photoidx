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
argparser.add_argument('--readOnly', 
                       help='access the index in read only mode', 
                       action='store_const', const=True)
argparser.add_argument('--create', 
                       help='create the index if not present', 
                       action='store_const', const=True)
photo.idxfilter.addFilterArguments(argparser)
args = argparser.parse_args()

app = QtGui.QApplication([])
try:
    idx = photo.index.Index(idxfile=args.directory)
    readOnly = args.readOnly
    dirty = False
except OSError:
    idx = photo.index.Index(imgdir=args.directory)
    if args.readOnly:
        readOnly = True
        dirty = False
    else:
        readOnly = not args.create
        dirty = args.create
idxfilter = photo.idxfilter.IdxFilter.from_args(args)
imageViewer = ImageViewer(idx, idxfilter, args.scale, readOnly, dirty)
sys.exit(app.exec_())
