#test file used to test put and get apis using django

import requests
from cache.views import put_in_db, get_from_db

put_api_url = 'http://127.0.0.1:8000/cache/put'
get_api_url = 'http://127.0.0.1:8000/cache/get'

data = [{"key": 4, "value": "3"}, {"key": 5, "value": "6"}, {"key": 6, "value": "8"}]
for pair in data:
    response = requests.put(put_api_url, data=pair)
    put_in_db(pair['key'], pair['value'])
print(response.json()) 

#hashMap: {4: 3, 5: 6, 6: 8}
#LinkedList: {{6:8}, {5,6}, {4,3}}


data = {"key": 5, "value": "7"}
response = requests.put(put_api_url, data=data)
put_in_db(data['key'], data['value'])
print(response.json()) 

#hashMap: {4: 3, 5: 7, 6: 8}
#LinkedList: {{5,7}, {6:8}, {4,3}}


data = {"key": 1, "value": "2"}
response = requests.put(put_api_url, data=data)
put_in_db(data['key'], data['value'])
print(response.json()) 

#hashMap: {5: 7, 6: 8, 1: 2}
#LinkedList: {{1,2}, {5,7}, {6,8}}


params = {"key": 6}
response = requests.get(get_api_url, params)
db_response = get_from_db(params['key'])
print(response.json())
print('DB Response: ', db_response.content)

#{'key': '6', 'value': '8'}

params = {"key": 0}
response = requests.get(get_api_url, params)
db_response = get_from_db(params['key'])
print(response.json())
print('DB Response: ', db_response.content)

#{'error': 'Key not found'}