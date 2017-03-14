# This file is part of audioread.
# Copyright 2017, Paul Brossier.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""Use aubio to read streams of audio data.

*Note*: using aubio this way is very inefficient, since the data will be
converted back from a numpy array of floats to a flat buffer of shorts.

"""

import aubio
from . import DecodeError

class AubioError(DecodeError):
    """ Aubio couldn't open that file."""

class AubioSource(aubio.source):
    """ Uses aubio to read media files or remote streams.

    To read a file, pass it to the constructor for AubioFile(), then iterate
    over the contents:

        >>> with AubioSource('something.flac') as f:
        >>>     print f.samplerate
        >>>     print f.channels
        >>>     print f.duration
        >>>     for block in f:
        >>>         do_something(block)

    """
    def __init__(self, filename):
        try:
            super().__init__(self, filename, 0)
        except RuntimeError as e:
            raise AubioError(e)

    def __next__(self):
        """ Override aubio.source.__next__ to convert back to int! """
        return (super().__next__().T * 32768).astype('int16').tobytes()

    @property
    def duration(self):
        """Length of the audio in seconds (a float)."""
        return float(super().duration) / self.samplerate
