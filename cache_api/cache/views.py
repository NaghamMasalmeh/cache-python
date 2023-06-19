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

put_api_url = 'http://127.0.0.1:8000/cache/put'
get_api_url = 'http://127.0.0.1:8000/cache/get'

cache_size = 3
cache = LRUCache(cache_size)

def index(request):
    return HttpResponse('Cache Homepage.')

#Memory Cache APIs
@csrf_exempt
def put_api(request):
    """
    This API is used to insert items to the cache
    """
    if request.method == 'PUT':
        #get key and value from request body and insert them to the cache
        data = request.body.decode('utf-8')
        data_dict = dict(item.split('=') for item in data.split('&'))
        if 'key' in data_dict and 'value' in data_dict:
            cache.put(data_dict['key'], data_dict['value'])
        return JsonResponse(cache.hash_map)

@csrf_exempt
def get_api(request):
    """"
    This API is used to get the value of the provided key from the cache
    """
    if request.method == 'GET':
        key = request.GET.get('key', None)
        if key is not None:
            if key in cache.hash_map:
                value = cache.hash_map.get(key)
                return value
            else:
                return None
        else:
            return JsonResponse({'error': 'Key is not provided'}, status=400)
