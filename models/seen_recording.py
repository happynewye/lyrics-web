
from mongoengine import *
import datetime

class SeenRecording(Document):
    mbid = StringField(required=True)
    seen_at = DateTimeField(default=datetime.datetime.now)
