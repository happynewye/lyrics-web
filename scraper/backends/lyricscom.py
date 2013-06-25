# Lyrics.com.
import re
import urllib

from scraper.backends.util import fetch_url, extract_text

from scraper.backends.util import URL_CHARACTERS
URL_PATTERN = 'http://www.lyrics.com/%s-lyrics-%s.html'
NOT_FOUND = (
    'Sorry, we do not have the lyric',
    'Submit Lyrics',
)

class LyricsCom(object):
    def fetch_lyrics(self, artist, title):
        """Fetch lyrics from Lyrics.com."""
        print('using lyricscom')
        url = URL_PATTERN % (self._lc_encode(title), self._lc_encode(artist))
        html = fetch_url(url)
        if not html:
            return

        lyrics = extract_text(html, '<div id="lyric_space">')
        if not lyrics:
            return
        for not_found_str in NOT_FOUND:
            if not_found_str in lyrics:
                return

        parts = lyrics.split('\n---\nLyrics powered by', 1)
        if parts:
            return parts[0]

    def _encode(self, s):
        """Encode the string for inclusion in a URL (common to both
        LyricsWiki and Lyrics.com).
        """
        if isinstance(s, str):
            for char, repl in list(URL_CHARACTERS.items()):
                s = s.replace(char, repl)
            s = s.encode('utf8', 'ignore')
        return urllib.parse.quote(s)

    def _lc_encode(self, s):
        s = re.sub(r'[^\w\s-]', '', s)
        s = re.sub(r'\s+', '-', s)
        return self._encode(s).lower()
