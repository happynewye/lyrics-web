from mongoengine import *
import datetime

class SeenQuery(Document):
    text = StringField(required=True)
    seen_at = DateTimeField(default=datetime.datetime.now)
