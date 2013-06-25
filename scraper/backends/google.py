import urllib
import json
import re
import difflib

API_KEY = 'AIzaSyBW4OJJvxMY-9YqK8I1hasZQ2PYvogyQgA'
ENGINE_ID = '009217259823014548361:lndtuqkycfu'

from scraper.backends.util import fetch_url, unescape, strip_cruft

class Google(object):
    """ A backend to scrape lyrics off any generic website.
    """
    def fetch_lyrics(self, artist, title):
        """Fetch lyrics from Google search results.
        """
        query = "%s %s" % (artist, title)
        print('using google')
        url = 'https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s' % \
            (API_KEY, ENGINE_ID, urllib.parse.quote(query.encode('utf8')))

        data = urllib.request.urlopen(url)
        data = data.read().decode()
        data = json.loads(data)
        if 'error' in data:
            reason = data['error']['errors'][0]['reason']
            log.debug('google lyrics backend error: %s' % reason)
            return None

        if 'items' in list(data.keys()):
            for item in data['items']:
                urlLink = item['link']
                urlTitle = item['title']
                if not self.is_page_candidate(urlLink, urlTitle, title, artist):
                    continue
                lyrics = self.scrape_lyrics_from_url(urlLink)
                if not lyrics:
                    continue

                lyrics = self.sanitize_lyrics(lyrics)

                if self.is_lyrics(lyrics, artist):
                    return lyrics
    
    def slugify(self, text):
        """Normalize a string and remove non-alphanumeric characters.
        """
        # TODO: exception logging

        # http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-
        # filename-in-python
        text = str(re.sub('[-\s]+', ' ', text))
        return urllib.parse.quote(text)

    def is_page_candidate(self, urlLink, urlTitle, title, artist):
        """Return True if the URL title makes it a good candidate to be a
        page that contains lyrics of title by artist.
        """
        title = self.slugify(title.lower())
        artist = self.slugify(artist.lower())
        sitename = re.search("//([^/]+)/.*", self.slugify(urlLink.lower())).group(1)
        urlTitle = self.slugify(urlTitle.lower())

        # Check if URL title contains song title (exact match)
        if urlTitle.find(title) != -1:
            return True
        # or try extracting song title from URL title and check if
        # they are close enough
        tokens = 'by%20'+artist + \
                str([artist, sitename, sitename.replace('www.','')]) + 'lyrics'
        songTitle = re.sub('(%s)' % '|'.join(tokens) ,'', urlTitle).strip('%20')


        typoRatio = .8
        return difflib.SequenceMatcher(None, songTitle, title).ratio() > typoRatio

    def insert_line_feeds(self, text):
        """Insert newlines before upper-case characters.
        """
        tokensStr = re.split("([a-z][A-Z])", text)
        for idx in range(1, len(tokensStr), 2):
            ltoken = list(tokensStr[idx])
            tokensStr[idx] = ltoken[0] + '\n' + ltoken[1]
        return ''.join(tokensStr)

    def sanitize_lyrics(self, text):
        """Clean text, returning raw lyrics as output or None if it happens
        that input text is actually not lyrics content.  Clean (x)html tags
        in text, correct layout and syntax...
        """
        text = strip_cruft(text, False)

        # Suppress advertisements.
        # Match lines with an opening bracket but no ending one, ie lines that
        # contained html link that has been wiped out when scraping.
        LINK1_RE = re.compile(r'(\(|\[).*[^\)\]]$')
        # Match lines containing url between brackets
        LINK2_RE = re.compile(r'(\(|\[).*[http|www].*(\]|\))')
        text = LINK1_RE.sub('', text)
        text = LINK2_RE.sub('', text)

        # Restore \n in input text
        if '\n' not in text:
            text = insert_line_feeds(text)

        while text.count('\n\n') > text.count('\n')/4:
            # Remove first occurrence of \n for each sequence of \n
            text = re.sub(r'\n(\n+)', '\g<1>', text)

        text = re.sub(r'\n\n+', '\n\n', text)   # keep at most two \n in a row

        return text

    def is_lyrics(self, text, artist):
        """Determine whether the text seems to be valid lyrics.
        """
        badTriggers = []
        nbLines = text.count('\n')
        if nbLines <= 1:
            log.debug("Ignoring too short lyrics '%s'" % text)
            return 0
        elif nbLines < 5:
            badTriggers.append('too_short')

        for item in artist, 'lyrics', 'copyright', 'property':
            badTriggers += [item] * len(re.findall(r'\W%s\W' % item, text, re.I))

        if badTriggers:
            log.debug('Bad triggers detected: %s' % badTriggers)

        return len(badTriggers) < 2

    def scrape_lyrics_from_url(self, url):
        """Scrape lyrics from a URL. If no lyrics can be found, return None
        instead.
        """
        from bs4 import BeautifulSoup, Tag, Comment
        html = fetch_url(url)
        soup = BeautifulSoup(html)

        for tag in soup.findAll('br'):
            tag.replaceWith('\n')

        # Remove non relevant html parts
        [s.extract() for s in soup(['head', 'script'])]
        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        [s.extract() for s in comments]

        try:
            for tag in soup.findAll(True):
                tag.name = 'p'          # keep tag contents

        except Exception as e:
            log.debug('Error %s when replacing containing marker by p marker' % e,
                exc_info=True)

        # Make better soup from current soup! The previous unclosed <p> sections
        # are now closed.  Use str() rather than prettify() as it's more
        # conservative concerning EOL
        soup = BeautifulSoup(str(soup))

        # In case lyrics are nested in no markup but <body>
        # Insert the whole body in a <p>
        bodyTag = soup.find('body')
        if bodyTag:
            pTag = soup.new_tag("p")
            bodyTag.parent.insert(0, pTag)
            pTag.insert(0, bodyTag)

        tagTokens = []

        for tag in soup.findAll('p'):
            soup2 = BeautifulSoup(str(tag))
            # Extract all text of <p> section.
            tagTokens += soup2.findAll(text=True)

        if tagTokens:
            # Lyrics are expected to be the longest paragraph
            tagTokens = sorted(tagTokens, key=len, reverse=True)
            soup = BeautifulSoup(tagTokens[0])
            return unescape(tagTokens[0].strip("\n\r: "))

