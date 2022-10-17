#! /usr/bin/python3
"""Try to find a partition of tags for a photo index.

Here, a partition of tags is defined as a set of tags such that each
item in the index is tagged with one and only one tag out of that
partition.

Note that such a partition may not exist for an index.  Furthermore,
the solution might not be unique, e.g. more then one partition may
exist for the same index.
"""

import photoidx.index


def tag_index(idx):
    """Return a mapping of tag names to index items.
    """
    tagidx = dict()
    for i in idx:
        for t in i.tags:
            if t not in tagidx:
                tagidx[t] = set()
            tagidx[t].add(i)
    return tagidx

def get_partition(idx):
    """Try to find a partition of tags for the index.

    The implementation follows an heuristic approach that is not
    guaranteed to find a solution, even if one exists.
    """
    tagidx = tag_index(idx)
    taglist = sorted(tagidx.keys(), key=lambda t: len(tagidx[t]), reverse=True)
    partition = set()
    covered = set()
    for t in taglist:
        if tagidx[t] & covered:
            continue
        partition.add(t)
        covered |= tagidx[t]
    if len(covered) == len(idx):
        # Found a solution
        return partition
    else:
        # Failed
        return None

if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    argparser.add_argument('-d', '--directory', 
                           help="image directory", default=".")
    args = argparser.parse_args()
    with photoidx.index.Index(idxfile=args.directory) as idx:
        partition = get_partition(idx)
        if partition:
            print("\n".join(partition))
