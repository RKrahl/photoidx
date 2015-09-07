#! /usr/bin/python

from __future__ import print_function
import argparse
import photo.index


def create(args):
    idx = photo.index.Index(imgdir=args.directory)
    idx.write()

def ls(args):
    idx = photo.index.Index(idxfile=args.directory)
    for i in idx:
        print(i.filename)

def md5(args):
    idx = photo.index.Index(idxfile=args.directory)
    for i in idx:
        print("%s  %s" % (i.md5, i.filename))


argparser = argparse.ArgumentParser()
argparser.add_argument('-d', '--directory', 
                       help="image directory", default=".")
subparsers = argparser.add_subparsers(title='subcommands')
create_parser = subparsers.add_parser('create', help="create the index")
create_parser.set_defaults(func=create)
ls_parser = subparsers.add_parser('ls', help="list image files")
ls_parser.set_defaults(func=ls)
md5_parser = subparsers.add_parser('md5', help="print md5 checksums")
md5_parser.set_defaults(func=md5)

args = argparser.parse_args()
args.func(args)
