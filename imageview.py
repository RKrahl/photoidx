#! /usr/bin/python

import sys
import argparse
from PySide import QtGui
from photo.viewer import ImageViewer

argparser = argparse.ArgumentParser()
argparser.add_argument('--scale', help="scale factor", default=(625.0/4096.0))
argparser.add_argument('images', help="image", nargs='*')
args = argparser.parse_args()

app = QtGui.QApplication([])
imageViewer = ImageViewer(args.images, scaleFactor=args.scale)
sys.exit(app.exec_())
