#! /usr/bin/python

import sys
import argparse
from PySide import QtGui
import photo.index
from photo.qt import ImageViewer

def strpdate(s):
    match = re.match(r"^(\d{1,})-(\d{1,2})-(\d{1,2})$", s)
    if match:
        y, m, d = match.group(1, 2, 3)
        try:
            return datetime.date(int(y), int(m), int(d))
        except ValueError:
            pass
    raise argparse.ArgumentTypeError("Invalid date value '%s'" % s)

argparser = argparse.ArgumentParser()
argparser.add_argument('-d', '--directory', help="image directory", default=".")
argparser.add_argument('--tags', help="select by comma separated list of tags")
argparser.add_argument('--date', type=strpdate, help="select by date")
argparser.add_argument('--scale', help="scale factor", default=(625.0/4096.0))
argparser.add_argument('files', nargs='*')
args = argparser.parse_args()

app = QtGui.QApplication([])
idx = photo.index.Index(idxfile=args.directory)
taglist = args.tags.split(",") if args.tags else []
imageViewer = ImageViewer(idx, taglist=taglist, date=args.date, 
                          filelist=args.files, scaleFactor=args.scale)
sys.exit(app.exec_())
