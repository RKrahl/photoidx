#! /usr/bin/python

from __future__ import print_function
import sys
import photo.index

idx = photo.index.Index(idxfile=sys.argv[1])
for i in idx:
    print("%s  %s" % (i.md5, i.filename))
