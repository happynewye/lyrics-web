from mongoengine import *

class Lyric(EmbeddedDocument):
    string = StringField(
            max_length=40000,
            required=True,
            unique=True
            )

    confidence = FloatField(
            min_value=0,
            max_value=1,
            default=1
            )

    views = IntField(
            min_value=0,
            default=0
            )

    downvotes = IntField(
            min_value=0,
            default=0
            )
    
    source = StringField(
            required=True
            )

    def __repr__(self):
        return self.string

    def __str__(self):
        return repr(self)
