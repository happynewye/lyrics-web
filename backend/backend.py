from mongoengine import connect
from models.song import Song
from pymongo import MongoClient
client = MongoClient()
db = client.test

connect('test')

class Backend(object):
    def get(self, _id):
        """Get a song by id.
        """
        song = Song.objects(id=_id)[0]
        return song

    def search(self, query, limit=10):
        """Full text search on mongodb.
        Also submit any search queries to be crawled.
        Returns a list of models.Song objects
        """
        #TODO: Hopefully mongoengine supports this soon.
        resultset = db.command(
                'text',         # text search
                'song',         # must be consistant with mongoengien
                search=query,
                project={
                    'lyric': 0, # conserve bandwidth?
                    },
                limit=limit
                )['results']

        #sort resultset by mongo full text search's score
        resultset = sorted(resultset, key=lambda x: x['score'], reverse=True)
        result = [Song(id=x['obj']['_id'],  **x['obj']) for x in resultset]
        # Also report search query
        self.enqueue_query(query)
        return result

    def enqueue_query(self, query):
        client.queue.query.insert({
                    'status': 'new',
                    'query': query,
                })
