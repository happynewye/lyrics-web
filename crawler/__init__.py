import musicbrainzngs as mb
from models.seen_query import SeenQuery
from models.seen_recording import SeenRecording
from models.song import Song
from mongoengine import connect
from time import sleep
from bson.objectid import ObjectId

from pymongo import MongoClient

client = MongoClient()

connect('test')

mb.set_useragent('lyrics app', '0.2', 'avoid3d@gmail.com')

from scraper import Scraper
scraper = Scraper()

class Crawler(object):
    def process_song(self, song):
        if (SeenRecording.objects(mbid=song.mbid)):
                return
        SeenRecording(mbid=song.mbid).save()
        if Song.objects(mbid=song.mbid):
            # We already have the song
            return
        lyric = scraper.get_lyrics(artist=song.artist, title=song.title)
        if lyric:
            song.add_lyric(lyric['string'], lyric['source'])
            song.save()

    def process_query(self, query):
        """Process a search query and add any lyrics
        that result to the database.
        """
        # Check if the query has been recently seen.
        if (SeenQuery.objects(text=query)):
            # If it has just return
            return

        # Otherwise cache the query now
        SeenQuery(text=' '.join(sorted(query.lower().split(' ')))).save()

        response = mb.search_recordings(query=query)['recording-list']
        results = [Song(
            title=x['title'],
            artist=x['artist-credit-phrase'],
            mbid=x['id']
            ) for x in response]

        print(len(results))
        results = set(results)
        print(len(results))

        for song in results:
            print('processing', song.title, 'by', song.artist)
            self.process_song(song)

    def listen(self, collection='query'):
        """Listen for new queries.
        """
        db = client.queue

        while(True):
            item = db.query.find_and_modify(
                query={'status': 'new'},
                update={'$set': {'status': 'processing'}},
                limit=1)

            if item:
                self.process_query(item['query'])
                db.query.update({'_id': ObjectId(item['_id'])}, {'$set': {'status': 'done'}})
            else:
                print('empty')
                sleep(1)
