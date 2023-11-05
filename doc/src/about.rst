About photoidx
==============

This package maintains indices for photo collections.  The index is
stored as a YAML file and contains metadata and tags describing the
photos.  The photos are accessed read only.

The purpose is to review photos in a collection, to annotate them with
tags and to select them.  In short, to create and to maintain metadata
about these photos.  The leading design goals are:

+ The photos should be accessed read only.  The image files should not
  be tampered with in any way.  That is why the metadata are not
  stored into the EXIF headers of the image files.

+ The storage of the metadata should be lightweight and simple.  We
  don't want to maintain complicated databases or proprietary binary
  files.

+ The GUI to review the photos should be easy to operate efficiently,
  using simple keyboard commands wherever possible.

It is assumed that the photo collection resides in one directory.
photoidx places a file ``.index.yaml`` in this directory to store the
metadata.  The format of this file is `YAML`_ which is a well
standardized, human-readable data serialization language.  The package
provides a command line tool and a graphical image viewer to create
and to manipulate this index.

.. _YAML: https://yaml.org/
