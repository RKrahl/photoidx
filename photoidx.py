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
        print(i.filename)

def md5(args):
    idx = photo.index.Index(idxfile=args.directory)
    taglist = args.tags.split(",") if args.tags else []
    for i in idx.filtered(taglist=taglist, filelist=args.files):
        print("%s  %s" % (i.md5, i.filename))

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
ls_parser.add_argument('--tags', help="comma separated list of tags")
ls_parser.add_argument('files', nargs='*')
ls_parser.set_defaults(func=ls)
md5_parser = subparsers.add_parser('md5', help="print md5 checksums")
md5_parser.add_argument('--tags', help="comma separated list of tags")
md5_parser.add_argument('files', nargs='*')
md5_parser.set_defaults(func=md5)
addtag_parser = subparsers.add_parser('addtag', help="add tag to images")
addtag_parser.add_argument('tag')
addtag_parser.add_argument('--tags', help="comma separated list of tags")
addtag_parser.add_argument('files', nargs='*')
addtag_parser.set_defaults(func=addtag)

args = argparser.parse_args()
args.func(args)
