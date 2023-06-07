#The main goal of the below application is to design a Cache Model
#The used replacement algorithm is Least Recently Used (LRU)
#To implement this, a combination of double linked list and a hash map (dictionary) is used
#hash map will be used to store the items, while the double linked list is used to manage the LRU algorithm
#by keeping the most recently used at the head of list while the LRU at the tail

#The idea behind using the hash map is that the complexity of search inside map is O(1)
#while inside the linked list is O(n)


from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .LRUcache import LRUCache
from pymongo import MongoClient
import time

mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client['cache_db']
collection = db['cache']
collection.delete_many({})

cache_size = 3
cache = LRUCache(cache_size)

def index(request):
    return HttpResponse("Cache Homepage.")

#Memory Cache APIs
@csrf_exempt
def put_api(request):
    """
    This API is used to insert items to the cache
    """
    if request.method == "PUT":
        #get key and value from request body and insert them to the cache
        data = request.body.decode('utf-8')
        data_dict = dict(item.split("=") for item in data.split("&"))
        if 'key' in data_dict and 'value' in data_dict:
            cache.put(data_dict['key'], data_dict['value'])
        return JsonResponse(cache.hash_map)

@csrf_exempt
def get_api(request):
    """"
    This API is used to get the value of the provided key from the cache
    """
    if request.method == "GET":
        key = request.GET.get('key', None)
        if key is not None:
            if key in cache.hash_map:
                value = cache.hash_map.get(key)
                return JsonResponse({'key': key, 'value': value})
            else:
                return JsonResponse({'error': 'Key not found'}, status=404)
        else:
            return JsonResponse({'error': 'Key is not provided'}, status=400)

#DB Cache APIs
def put_in_db(key, value):
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

def get_from_db(key):
    """
    Get the key for the required docuemnt, and search in the db
    if the key exists it will return its value
    """
    cache_item = collection.find_one({'key': key})
    if cache_item is None:
        return JsonResponse({'error': 'Key not found'})
    else:
        return JsonResponse({'key': key, 'value': cache_item['value']})
