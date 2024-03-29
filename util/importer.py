from pymongo import MongoClient
from models.song import Song
from mongoengine import connect

connect('test')

client = MongoClient()
db = client.test

print('hello')
for n_song in db.target.find():
    mbid = n_song.get('mbid', None)
    if not mbid:
        continue
    song = Song.objects(mbid=mbid)
    if not song:
        song = Song(
                mbid=mbid,
                title=n_song['title'],
                artist=n_song['artist']
                )

    song.add_lyric(n_song.get('lyric', None), 'target')
    song.save()
