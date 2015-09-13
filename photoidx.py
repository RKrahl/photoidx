#! /usr/bin/python

from __future__ import print_function
import argparse
import photo.index


def create(args):
    idx = photo.index.Index(imgdir=args.directory)
    idx.write()

def ls(args):
    idx = photo.index.Index(idxfile=args.directory)
    taglist = args.tags.split(",") if args.tags else []
    for i in idx.filtered(taglist=taglist, filelist=args.files):
        if args.md5:
            print("%s  %s" % (i.md5, i.filename))
        else:
            print(i.filename)

def addtag(args):
    idx = photo.index.Index(idxfile=args.directory)
    taglist = args.tags.split(",") if args.tags else []
    for i in idx.filtered(taglist=taglist, filelist=args.files):
        i.tags.add(args.tag)
    idx.write()


argparser = argparse.ArgumentParser()
argparser.add_argument('-d', '--directory', 
                       help="image directory", default=".")
subparsers = argparser.add_subparsers(title='subcommands')
create_parser = subparsers.add_parser('create', help="create the index")
create_parser.set_defaults(func=create)
ls_parser = subparsers.add_parser('ls', help="list image files")
ls_parser.add_argument('--md5', action='store_true', help="print md5 checksums")
ls_parser.add_argument('--tags', help="comma separated list of tags")
ls_parser.add_argument('files', nargs='*')
ls_parser.set_defaults(func=ls)
addtag_parser = subparsers.add_parser('addtag', help="add tag to images")
addtag_parser.add_argument('tag')
addtag_parser.add_argument('--tags', help="comma separated list of tags")
addtag_parser.add_argument('files', nargs='*')
addtag_parser.set_defaults(func=addtag)

args = argparser.parse_args()
args.func(args)
