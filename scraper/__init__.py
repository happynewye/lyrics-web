# This file is inspired by part of beets
# Copyright 2013, Adrian Sampson.
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

"""Fetches, embeds, and displays lyrics.
"""
import re
import logging
import urllib.request, urllib.parse, urllib.error
import json
import unicodedata
import difflib

from scraper.backends.google import Google
from scraper.backends.lyricswiki import LyricsWiki
from scraper.backends.lyricscom import LyricsCom

from scraper.utils import remove_featuring

class Scraper(object):
    """ Used to scrape lyrics off the internet.
    """
    def __init__(self):
        self.backends = [
                LyricsWiki(),
                LyricsCom(),
                #TODO: priority
                #Google(),
                ]

    def get_lyrics(self, artist, title):
        """Fetch lyrics, trying each source in turn. Return a string or
        None if no lyrics were found.
        """
        artist = remove_featuring(artist)

        for backend in self.backends:
            lyrics = backend.fetch_lyrics(artist, title)
            if lyrics:
                #if isinstance(lyrics, bytes):
                #    lyrics = lyrics.decode('utf8', 'ignore')
                return {
                        'string': lyrics,
                        'source': repr(backend)
                        }

