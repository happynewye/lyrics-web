from pymongo import MongoClient
import time
from datetime import datetime
client = MongoClient()

class Source(object):
    """All events are associated with a source.
    """
    def __init__(self, name, db=client['pontus']):
        self.db = db
        self.collection = self.db[name]
        self.aggregates = self.collection['aggregates']
        self.name = name

        self.db.sources.update(
                {
                    'source_name': self.name
                },
                {
                    '$set': {
                        'source_name': self.name
                    }
                },
                upsert=True
                )

    def track(self, event_name, **kwargs):
        kwargs['event_name'] = event_name
        self.collection.insert(kwargs)

        now = datetime.now()
        min_bucket = now.strftime('%Y-%m-%d-%H-%M')

        self.aggregates.update(
                {
                    'event_name': event_name,
                    'min_bucket': min_bucket,
                    'milis': (time.mktime(datetime.now().timetuple()) // 60) * 60000,
                },
                {'$inc': {'count': 1}},
                upsert=True
                )
