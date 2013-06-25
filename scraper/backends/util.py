"""Helper methods used by the backend to
scrape content.
"""

import urllib
import re

COMMENT_RE = re.compile(r'<!--.*-->', re.S)
BREAK_RE = re.compile(r'<br\s*/?>')
TAG_RE = re.compile(r'<[^>]*>')
DIV_RE = re.compile(r'<(/?)div>?')
FETCH_URL_TIMEOUT=5

URL_CHARACTERS = {
    '\u2018': "'",
    '\u2019': "'",
    '\u201c': '"',
    '\u201d': '"',
    '\u2010': '-',
    '\u2011': '-',
    '\u2012': '-',
    '\u2013': '-',
    '\u2014': '-',
    '\u2015': '-',
    '\u2016': '-',
    '\u2026': '...',
}

def fetch_url(url):
    """Retrieve the content at a given URL, or return None if the source
    is unreachable.
    """
    # TODO: handle this error more gracefully
    return urllib.request.urlopen(url, timeout=FETCH_URL_TIMEOUT).read()

def unescape(text):
    """Resolves &#xxx; HTML entities (and some others)."""
    if isinstance(text, bytes):
        text = text.decode('utf8', 'ignore')
    out = text.replace('&nbsp;', ' ')
    def replchar(m):
        num = m.group(1)
        return chr(int(num))
    out = re.sub("&#(\d+);", replchar, out)
    return out

def extract_text(html, starttag):
    """Extract the text from a <DIV> tag in the HTML starting with
    ``starttag``. Returns None if parsing fails.
    """
    # Strip off the leading text before opening tag.
    try:
        html = html.decode('utf-8')
        _, html = html.split(starttag, 1)
    except ValueError:
        return

    # Walk through balanced DIV tags.
    level = 0
    parts = []
    pos = 0
    for match in DIV_RE.finditer(html):
        if match.group(1): # Closing tag.
            level -= 1
            if level == 0:
                pos = match.end()
        else: # Opening tag.
            if level == 0:
                parts.append(html[pos:match.start()])

            level += 1

        if level == -1:
            parts.append(html[pos:match.start()])
            break
    else:
        print('no closing tag found!')
        return
    lyrics = ''.join(parts)
    return strip_cruft(lyrics)

def strip_cruft(lyrics, wscollapse=False):
    """Clean up HTML from an extracted lyrics string. For example, <BR>
    tags are replaced with newlines.
    """
    # TODO: decide how to handle newlines
    lyrics = COMMENT_RE.sub('', lyrics)
    lyrics = unescape(lyrics)
    if wscollapse:
        lyrics = re.sub(r'\s+', ' ', lyrics) # Whitespace collapse.
    lyrics = BREAK_RE.sub('\n', lyrics) # <BR> newlines.
    lyrics = re.sub(r'\n +', '\n', lyrics)
    lyrics = re.sub(r' +\n', '\n', lyrics)
    lyrics = TAG_RE.sub('', lyrics) # Strip remaining HTML tags.
    lyrics = lyrics.replace('\r','\n')
    lyrics = lyrics.strip()
    return lyrics
