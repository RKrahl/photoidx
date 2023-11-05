Selection options
~~~~~~~~~~~~~~~~~

The following options may be used to select the images.

   ``--tags TAGS``
      Select images by tags.  *TAGS* should be a comma separated list
      of tags.  Individual tags may be negated by prepending them with
      an exclamation mark.  This option selects the images that have
      all the listed tags, but none of the negated tags.  If *TAGS* is
      the empty string, the option selects the images that have no
      tags set.

      Examples::

	--tags 'Tokyo,Imperial_Palace,Cherry_blossoms'
	--tags 'Tokyo,!Ginza'
	--tags ''

      The first example selects all images that are tagged with
      ``Tokyo``, ``Imperial_Palace``, and with ``Cherry_blossoms``.
      The second example selects images tagged with ``Tokyo``, but not
      with ``Ginza``.  The last example selects images that have no
      tags at all.

   ``--date DATE``
      Select images by creation date.  *DATE* may either be a single
      date or a date interval in ISO 8601 format (not all variants of
      ISO 8601 are supported though).  The start and end date may
      optionally also indicate a time of day.  If *DATE* is a single
      date without time of day, the option selects images taken this
      day.  If it is a single date including time of day, the option
      selects only images taken at this particular moment.  If *DATE*
      is a date interval, the option selects the images that were
      taken within this interval.  In this case, if the start or the
      end date do not indicate a time of day, the time defaults to
      beginning or end of the day respectively.

      Examples::

	--date '2015-03-14'
	--date '2015-03-14T09:26:53'
	--date '2016-02-28/2016-03-04'
	--date '2016-02-28T15:30:01/2016-03-04T14:15:41'

      The first example selects all images taken on the 14th of
      March 2015.  The second one selects images taken at 9:26:53
      a.m. at the same day.  The third example selects images taken in
      the time from beginning of 28th of February until end of 4th of
      March 2016.  The last example adds precise times of the day to
      the date interval.

      .. note::
	 The time of creation is taken from the EXIF data of the
	 image.  This EXIF time does not contain any time zone
	 information.  The time is generally considered to be local
	 time of the place where the image is taken.  As a
	 consequence, the ``--date`` option does not support time zone
	 designators.

   ``--gpspos GPSPOS``
      Select images by GPS position.  *GPSPOS* should be a geographic
      location with the latitude and longitude separated by a comma.
      Latitude and longitude should be positive floating point numbers
      with a suffix for the direction, ``N`` or ``S`` for the latitude
      and ``E`` or ``W`` for the longitude.  The option selects images
      with a GPS position within a certain distance of this location.
      The radius of this selection defaults to 3 km and may be set
      with ``--gpsradius``.

      Example::

	--gpspos '52.5186 N, 13.4081 E'

      This select images taken within a distance of up to 3 km of
      Berlin City Hall.

   ``--gpsradius DISTANCE``
      Radius around the GPS position in km.  *DISTANCE* should be a
      floating point number.  This option is only relevant if
      ``--gpspos`` is set as well.

      Example::

	--gpspos '52.5186 N, 13.4081 E' --gpsradius 20.0

      This select images taken within a distance of up to 20 km of
      Berlin City Hall.

   ``files``
      Select images by file name.  *files* should be a white space
      separated list of file names.  This selects the images whose
      file name appears in the list.

If more then one selection option is given, only the images that meet
all the criteria are selected.  If no selection option is given, all
images in the index or in the directory are selected.
