#The main goal of the below application is to design a Cache Model
#The used replacement algorithm is Least Recently Used (LRU)
#To implement this, a combination of double linked list and a hash map (dictionary) is used
#hash map will be used to store the items, while the double linked list is used to manage the LRU algorithm
#by keeping the most recently used at the head of list while the LRU at the tail

#The idea behind using the hash map is that the complexity of search inside map is O(1)
#while inside the linked list is O(n)


import requests, json
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .LRUcache import LRUCache
import urllib.parse

cache = LRUCache(3)

def index(request):
    return HttpResponse("Cache Homepage.")

@csrf_exempt
def put_api(request):
    if request.method == "PUT":
        data = request.body.decode('utf-8')
        data_dict = dict(item.split("=") for item in data.split("&"))
        if 'key' in data_dict and 'value' in data_dict:
            cache.put(data_dict['key'], data_dict['value'])
        return JsonResponse(cache.hash_map)

@csrf_exempt
def get_api(request):
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
