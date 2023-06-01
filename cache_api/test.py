#test file used to test put and get apis using django

import requests
import json

put_api_url = 'http://127.0.0.1:8000/cache/put'
get_api_url = 'http://127.0.0.1:8000/cache/get'

data = [{"key": "4", "value": "3"}, {"key": "5", "value": "6"}, {"key": "6", "value": "8"}]
for pair in data:
    response = requests.put(put_api_url, data=pair)
print(response.json()) 
#hashMap: {4: 3, 5: 6, 6: 8}
#LinkedList: {{6:8}, {5,6}, {4,3}}


data = {"key": "5", "value": "7"}
response = requests.put(put_api_url, data=data)
print(response.json()) 

#hashMap: {4: 3, 5: 7, 6: 8}
#LinkedList: {{5,7}, {6:8}, {4,3}}


data = {"key": "1", "value": "2"}
response = requests.put(put_api_url, data=data)
print(response.json()) 

#hashMap: {5: 7, 6: 8, 1: 2}
#LinkedList: {{1,2}, {5,7}, {6,8}}


# Define the parameters for the GET request
params = {"key": "6"}
response = requests.get(get_api_url, params)
print(response.json()) 

#{'key': '6', 'value': '8'}

params = {"key": "0"}
response = requests.get(get_api_url, params)
print(response.json())

#{'error': 'Key not found'}