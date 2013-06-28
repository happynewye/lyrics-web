import json
from flask import current_app, request

from pymongo import MongoClient, DESCENDING
client = MongoClient()
db = client['pontus']

def to_dict(record):
    return {'name': record['source_name']}

@current_app.route('/api/sources')
def sources():
    cursor = db.sources.find()
    source_list = [to_dict(x) for x in cursor]
    data = {'sources': source_list}
    return json.dumps(data)
