import json
from flask import current_app, request

from pymongo import MongoClient, DESCENDING
client = MongoClient()
db = client['pontus']

def to_dict(record):
    return {
            'name': record['_id'],
            'buckets': record['buckets']
            }

@current_app.route('/api/data')
def data():
    source_name = request.args.get('name')
    collection = db[source_name]['aggregates']
    cursor = collection.aggregate([
        {'$group': {
            '_id': '$event_name',
            'buckets': {
                '$push': {
                    'count': '$count',
                    'milis': '$milis'
                    }
                }
            }
        }])

    data = [to_dict(record) for record in cursor['result']] 
    return json.dumps(data)
