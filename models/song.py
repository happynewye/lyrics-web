from mongoengine import *
from difflib import SequenceMatcher as fuzzy

from models.lyric import Lyric

class Song(Document):
    title = StringField(
            max_length=200,
            required=True
            )

    artist = StringField(
            max_length=200,
            required=True
            )

    # Globaly unique uuid
    mbid = StringField(
            max_length=36,
            unique=True,
            required=True)

    lyrics = ListField(EmbeddedDocumentField(Lyric))

    def add_lyric(self, new_lyric_string, source):
        # check if new lyric is similar enough to
        # old lyric to be considered the same.
        for lyric in self.lyrics:
            if (fuzzy(None, lyric.string, new_lyric_string).ratio() > 0.9):
                return False
        self.lyrics.insert(0, Lyric(string=new_lyric_string, source=source, confidence=1))
        return True

    def get_best_lyric(self):
        """Gets the lyric we are most confident in.
        """
        results = sorted(self.lyrics)
        return str(results[0])

    def __hash__(self):
        return hash(repr(self.artist) + repr(self.title))

    def __eq__(self, other):
        return repr(self.artist) == repr(other.artist) and repr(self.title) == repr (other.title)

    def __repr__(self):
        return self.title + ' by ' + self.artist

    def __str__(self):
        return repr(self)
