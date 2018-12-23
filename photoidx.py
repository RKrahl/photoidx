#! /usr/bin/python

from __future__ import print_function
import argparse
import photo.index
import photo.idxfilter
from photo.stats import Stats


def create(args):
    idxfile = args.directory if args.update else None
    hashalg = args.checksums.split(',') if args.checksums else []
    idx = photo.index.Index(idxfile=idxfile, imgdir=args.directory, 
                            hashalg=hashalg)
    idx.write()

def ls(args):
    idx = photo.index.Index(idxfile=args.directory)
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    for i in idxfilter.filter(idx):
        if args.checksum:
            try:
                checksum = i.checksum[args.checksum]
            except KeyError:
                continue
            print("%s  %s" % (checksum, i.filename))
        else:
            print(i.filename)

def lstags(args):
    idx = photo.index.Index(idxfile=args.directory)
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    tags = set()
    for i in idxfilter.filter(idx):
        tags.update(i.tags)
    for t in sorted(tags):
        print(t)

def addtag(args):
    idx = photo.index.Index(idxfile=args.directory)
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    for i in idxfilter.filter(idx):
        i.tags.add(args.tag)
    idx.write()

def rmtag(args):
    idx = photo.index.Index(idxfile=args.directory)
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    for i in idxfilter.filter(idx):
        i.tags.discard(args.tag)
    idx.write()

def select(args):
    idx = photo.index.Index(idxfile=args.directory)
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    for i in idxfilter.filter(idx):
        i.selected = True
    idx.write()

def deselect(args):
    idx = photo.index.Index(idxfile=args.directory)
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    for i in idxfilter.filter(idx):
        i.selected = False
    idx.write()

def stats(args):
    idx = photo.index.Index(idxfile=args.directory)
    idxfilter = photo.idxfilter.IdxFilter.from_args(args)
    stats = Stats(idxfilter.filter(idx))
    print(str(stats))


argparser = argparse.ArgumentParser()
argparser.add_argument('-d', '--directory', 
                       help="image directory", default=".")
subparsers = argparser.add_subparsers(title='subcommands')

create_parser = subparsers.add_parser('create', help="create the index")
create_parser.add_argument('--checksums', default="md5", 
                           help=("comma separated list of "
                                 "hash algorithms to calculate checksums"))
create_parser.add_argument('--update', action='store_true', 
                           help="add images to an existing index")
create_parser.set_defaults(func=create)

ls_parser = subparsers.add_parser('ls', help="list image files")
ls_parser.add_argument('--checksum', help="hash algorithm to print checksums")
photo.idxfilter.addFilterArguments(ls_parser)
ls_parser.set_defaults(func=ls)

lstags_parser = subparsers.add_parser('lstags', help="list tags")
photo.idxfilter.addFilterArguments(lstags_parser)
lstags_parser.set_defaults(func=lstags)

addtag_parser = subparsers.add_parser('addtag', help="add tag to images")
addtag_parser.add_argument('tag')
photo.idxfilter.addFilterArguments(addtag_parser)
addtag_parser.set_defaults(func=addtag)

rmtag_parser = subparsers.add_parser('rmtag', help="remove tag from images")
rmtag_parser.add_argument('tag')
photo.idxfilter.addFilterArguments(rmtag_parser)
rmtag_parser.set_defaults(func=rmtag)

select_parser = subparsers.add_parser('select', 
                                      help="add images to the selection")
photo.idxfilter.addFilterArguments(select_parser)
select_parser.set_defaults(func=select)

deselect_parser = subparsers.add_parser('deselect', 
                                        help="remove images from the selection")
photo.idxfilter.addFilterArguments(deselect_parser)
deselect_parser.set_defaults(func=deselect)

stats_parser = subparsers.add_parser('stats', help="show statistics")
photo.idxfilter.addFilterArguments(stats_parser)
stats_parser.set_defaults(func=stats)

args = argparser.parse_args()
args.func(args)
