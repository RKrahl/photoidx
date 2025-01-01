#! /usr/bin/python

import argparse
from photoidx.datetools import gettz
import photoidx.index
import photoidx.idxfilter
from photoidx.stats import Stats


def create(args):
    kwargs = dict(
        idxfile = None,
        imgdir = args.directory,
        checksums = args.checksums.split(',') if args.checksums else [],
        comment = args.comment,
        default_tz = args.timezone,
    )
    with photoidx.index.Index(**kwargs) as idx:
        idx.write()

def update(args):
    kwargs = dict(
        idxfile = args.directory,
        imgdir = args.directory,
        checksums = None,
        comment = args.comment,
        default_tz = args.timezone,
    )
    with photoidx.index.Index(**kwargs) as idx:
        idx.write()

def ls(args):
    with photoidx.index.Index(idxfile=args.directory) as idx:
        idxfilter = photoidx.idxfilter.IdxFilter.from_args(idx, args)
        for i in idxfilter.filter():
            if args.checksum:
                try:
                    checksum = i.checksum[args.checksum]
                except KeyError:
                    continue
                print("%s  %s" % (checksum, i.filename))
            else:
                print(i.filename)

def lstags(args):
    with photoidx.index.Index(idxfile=args.directory) as idx:
        idxfilter = photoidx.idxfilter.IdxFilter.from_args(idx, args)
        tags = set()
        for i in idxfilter.filter():
            tags.update(i.tags)
        for t in sorted(tags):
            print(t)

def addtag(args):
    with photoidx.index.Index(idxfile=args.directory) as idx:
        idxfilter = photoidx.idxfilter.IdxFilter.from_args(idx, args)
        for i in idxfilter.filter():
            i.tags.add(args.tag)
        idx.write()

def rmtag(args):
    with photoidx.index.Index(idxfile=args.directory) as idx:
        idxfilter = photoidx.idxfilter.IdxFilter.from_args(idx, args)
        for i in idxfilter.filter():
            i.tags.discard(args.tag)
        idx.write()

def select(args):
    with photoidx.index.Index(idxfile=args.directory) as idx:
        idxfilter = photoidx.idxfilter.IdxFilter.from_args(idx, args)
        for i in idxfilter.filter():
            i.selected = True
        idx.write()

def deselect(args):
    with photoidx.index.Index(idxfile=args.directory) as idx:
        idxfilter = photoidx.idxfilter.IdxFilter.from_args(idx, args)
        for i in idxfilter.filter():
            i.selected = False
        idx.write()

def stats(args):
    with photoidx.index.Index(idxfile=args.directory) as idx:
        idxfilter = photoidx.idxfilter.IdxFilter.from_args(idx, args)
        stats = Stats(idxfilter.filter())
        print(str(stats))


argparser = argparse.ArgumentParser()
argparser.add_argument('-d', '--directory', 
                       help="image directory", default=".")
subparsers = argparser.add_subparsers(title='subcommands')

create_parser = subparsers.add_parser('create', help="create the index")
create_parser.add_argument('--comment', help="Comment text")
create_parser.add_argument('--timezone',
                           help="Time zone to set for image create time",
                           type=gettz, default=gettz())
create_parser.add_argument('--checksums', default="md5", 
                           help=("comma separated list of "
                                 "hash algorithms to calculate checksums"))
create_parser.set_defaults(func=create)

update_parser = subparsers.add_parser('update',
                                      help="add images to an existing index")
update_parser.add_argument('--comment', help="Comment text")
update_parser.add_argument('--timezone',
                           help="Time zone to set for image create time",
                           type=gettz, default=gettz())
update_parser.set_defaults(func=update)

ls_parser = subparsers.add_parser('ls', help="list image files")
ls_parser.add_argument('--checksum', help="hash algorithm to print checksums")
photoidx.idxfilter.addFilterArguments(ls_parser)
ls_parser.set_defaults(func=ls)

lstags_parser = subparsers.add_parser('lstags', help="list tags")
photoidx.idxfilter.addFilterArguments(lstags_parser)
lstags_parser.set_defaults(func=lstags)

addtag_parser = subparsers.add_parser('addtag', help="add tag to images")
addtag_parser.add_argument('tag')
photoidx.idxfilter.addFilterArguments(addtag_parser)
addtag_parser.set_defaults(func=addtag)

rmtag_parser = subparsers.add_parser('rmtag', help="remove tag from images")
rmtag_parser.add_argument('tag')
photoidx.idxfilter.addFilterArguments(rmtag_parser)
rmtag_parser.set_defaults(func=rmtag)

select_parser = subparsers.add_parser('select', 
                                      help="add images to the selection")
photoidx.idxfilter.addFilterArguments(select_parser)
select_parser.set_defaults(func=select)

deselect_parser = subparsers.add_parser('deselect', 
                                        help="remove images from the selection")
photoidx.idxfilter.addFilterArguments(deselect_parser)
deselect_parser.set_defaults(func=deselect)

stats_parser = subparsers.add_parser('stats', help="show statistics")
photoidx.idxfilter.addFilterArguments(stats_parser)
stats_parser.set_defaults(func=stats)

args = argparser.parse_args()
if not hasattr(args, "func"):
    argparser.error("subcommand is required")
args.func(args)
