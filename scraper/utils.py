import re

def remove_featuring(artist):
        """A helper method to Remove featuring artists
        from a string describing the artists for a
        recording.
        """
        # TODO: There are other ways of adding cruft to
        # the artist's field.
        pattern = "(.*) feat(uring|\.)?\s\S+"
        match = re.search(pattern, artist, re.IGNORECASE)
        if match:
            artist = match.group(0)
        return artist
