from django.http import HttpResponse
from pymongo import MongoClient
from .views import cache_size
import time

conn_string = "mongodb+srv://naghammasalmah:mongodb@cluster0.utxq31t.mongodb.net/?retryWrites=true&w=majority"
mongo_client = MongoClient(conn_string, port=27017)

db = mongo_client['cache_db']
collection = db['cache']

#DB Cache APIs
def put_in_db(key: int, value: any) -> HttpResponse:
    """
    Insert key-value pair to the db, if the number of documents inside db is greater than cache size
    it will remove the LRU by finding the document with the oldest access time.
    """
    documents_count = collection.count_documents({})
    if documents_count == cache_size:
        oldest_document = collection.find_one(sort=[('access_time', 1)], limit=1)
        collection.delete_one({'_id': oldest_document['_id']})
    collection.update_one({'key': key}, {'$set': {'value': value, 'access_time': time.time()}}, upsert=True)
    return HttpResponse({'Document successfully inserted to the DB!'})


def get_from_db(key: int) -> any:
    """
    Get the key for the required docuemnt, and search in the db
    if the key exists it will return its value
    """
    cache_item = collection.find_one({'key': key})
    if cache_item is None:
        return None
    else:
        return cache_item['value']