"""Backend for retrieving lyrics from lyrics.wikia.com.
"""
import re
import urllib

from urllib.error import HTTPError

from scraper.backends.util import fetch_url, extract_text

from scraper.backends.util import URL_CHARACTERS
LYRICSWIKI_URL_PATTERN = 'http://lyrics.wikia.com/%s:%s'

class LyricsWiki(object):
    def fetch_lyrics(self, artist, title):
        print('using lyricswiki')
        """Fetch lyrics from LyricsWiki."""
        url = LYRICSWIKI_URL_PATTERN % (self._lw_encode(artist), self._lw_encode(title))
        try:
            html = fetch_url(url)
        except HTTPError:
            return
        if not html:
            return

        lyrics = extract_text(html, "<div class='lyricbox'>")
        if lyrics and 'Unfortunately, we are not licensed' not in lyrics:
            return lyrics

    def _encode(self, s):
        """Encode the string for inclusion in a URL (common to both
        LyricsWiki and Lyrics.com).
        """
        if isinstance(s, str):
            for char, repl in list(URL_CHARACTERS.items()):
                s = s.replace(char, repl)
            s = s.encode('utf8', 'ignore')
        return urllib.parse.quote(s)

    def _lw_encode(self, s):
        s = re.sub(r'\s+', '_', s)
        s = s.replace("<", "Less_Than")
        s = s.replace(">", "Greater_Than")
        s = s.replace("#", "Number_")
        s = re.sub(r'[\[\{]', '(', s)
        s = re.sub(r'[\]\}]', ')', s)
        return self._encode(s)
