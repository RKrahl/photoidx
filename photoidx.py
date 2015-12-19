#! /usr/bin/python

from __future__ import print_function
import re
import datetime
import argparse
import photo.index


def strpdate(s):
    match = re.match(r"^(\d{1,})-(\d{1,2})-(\d{1,2})$", s)
    if match:
        y, m, d = match.group(1, 2, 3)
        try:
            return datetime.date(int(y), int(m), int(d))
        except ValueError:
            pass
    raise argparse.ArgumentTypeError("Invalid date value '%s'" % s)


def create(args):
    idx = photo.index.Index(imgdir=args.directory)
    idx.write()

def ls(args):
    idx = photo.index.Index(idxfile=args.directory)
    taglist = args.tags.split(",") if args.tags else []
    for i in idx.filtered(taglist=taglist, date=args.date, filelist=args.files):
        if args.md5:
            print("%s  %s" % (i.md5, i.filename))
        else:
            print(i.filename)

def lstags(args):
    idx = photo.index.Index(idxfile=args.directory)
    taglist = args.tags.split(",") if args.tags else []
    tags = set()
    for i in idx.filtered(taglist=taglist, date=args.date, filelist=args.files):
        tags.update(i.tags)
    for t in sorted(tags):
        print(t)

def addtag(args):
    idx = photo.index.Index(idxfile=args.directory)
    taglist = args.tags.split(",") if args.tags else []
    for i in idx.filtered(taglist=taglist, date=args.date, filelist=args.files):
        i.tags.add(args.tag)
    idx.write()

def rmtag(args):
    idx = photo.index.Index(idxfile=args.directory)
    taglist = args.tags.split(",") if args.tags else []
    for i in idx.filtered(taglist=taglist, date=args.date, filelist=args.files):
        i.tags.discard(args.tag)
    idx.write()


argparser = argparse.ArgumentParser()
argparser.add_argument('-d', '--directory', 
                       help="image directory", default=".")
subparsers = argparser.add_subparsers(title='subcommands')
create_parser = subparsers.add_parser('create', help="create the index")
create_parser.set_defaults(func=create)

ls_parser = subparsers.add_parser('ls', help="list image files")
ls_parser.add_argument('--md5', action='store_true', help="print md5 checksums")
ls_parser.add_argument('--tags', help="select by comma separated list of tags")
ls_parser.add_argument('--date', type=strpdate, help="select by date")
ls_parser.add_argument('files', nargs='*')
ls_parser.set_defaults(func=ls)

lstags_parser = subparsers.add_parser('lstags', help="list tags")
lstags_parser.add_argument('--tags', 
                           help="select by comma separated list of tags")
lstags_parser.add_argument('--date', type=strpdate, help="select by date")
lstags_parser.add_argument('files', nargs='*')
lstags_parser.set_defaults(func=lstags)

addtag_parser = subparsers.add_parser('addtag', help="add tag to images")
addtag_parser.add_argument('tag')
addtag_parser.add_argument('--tags', 
                           help="select by comma separated list of tags")
addtag_parser.add_argument('--date', type=strpdate, help="select by date")
addtag_parser.add_argument('files', nargs='*')
addtag_parser.set_defaults(func=addtag)

rmtag_parser = subparsers.add_parser('rmtag', help="remove tag from images")
rmtag_parser.add_argument('tag')
rmtag_parser.add_argument('--tags', 
                          help="select by comma separated list of tags")
rmtag_parser.add_argument('--date', type=strpdate, help="select by date")
rmtag_parser.add_argument('files', nargs='*')
rmtag_parser.set_defaults(func=rmtag)

args = argparser.parse_args()
args.func(args)
