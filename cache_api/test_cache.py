#Test file used to test put and get data from mongodb and cache memory
#set DJANGO_SETTINGS_MODULE=cache_api.settings

import requests, json, pytest
from typing import List
from django.http import HttpResponse
from cache.mongo import put_in_db, get_from_db, collection
from cache.views import put_api_url, get_api_url

test_data = [{'key': 4, 'value': '3'}, {'key': 5, 'value': '6'}, {'key': 6, 'value': '8'}]
test_data_with_evicted_value = [{'key': 5, 'value': '6'}, {'key': 6, 'value': '8'}, {'key': 1, 'value': '2'}]
test_data_with_updated_value = [{'key': 6, 'value': '8'}, {'key': 1, 'value': '2'}, {'key': 5, 'value': '7'}]
updated_data = {'key': 5, 'value': '7'}
new_data = {'key': 1, 'value': '2'}


def add_data_to_db_and_cache(data: dict) -> dict:
    """
    Add data to the cache memory and database and return the hash map for the cache memory 
    """
    api_response = requests.put(put_api_url, data=data)
    put_in_db(data['key'], data['value'])
    return api_response


def compare_api_data(actual_data: dict, expected_data: List[dict]):
    """
    Compare expected data with data returned from the api call when add items to cache memory
    """
    dict_expected_data = {str(d['key']): d['value'] for d in expected_data}
    assert actual_data == dict_expected_data


def compare_db_data(actual_data: List[dict], expected_data: List[dict]):
    """
    Compare expected data with data returned from the db
    """
    for i, data in enumerate(actual_data):
        assert data['key'] == expected_data[i]['key']
        assert data['value'] == expected_data[i]['value']


def check_data(api_response: HttpResponse, test_data: List[dict]) -> None:
    """
    Compare expected data with data returned from the db and cache memory
    """
    response = json.loads(api_response.content.decode('utf-8'))
    compare_api_data(response, test_data)

    result = collection.find({})
    compare_db_data(list(result), test_data)


def test_add_data_to_db_and_cache():
    """
    Test adding data to the db and memory and check the response with the expected data
    """
    api_response = None
    for data in test_data:
        api_response = add_data_to_db_and_cache(data)
    check_data(api_response, test_data)


def test_evict_item_in_db_and_cache():
    """
    Test the LRU algorithm by removing the LRU item from the cache
    """
    api_response = add_data_to_db_and_cache(new_data)
    check_data(api_response, test_data_with_evicted_value)


def test_update_item_in_db_and_cache():
    """
    Test Updating item in the db and memory
    """
    api_response = add_data_to_db_and_cache(updated_data)
    check_data(api_response, test_data_with_updated_value)


@pytest.mark.parametrize('key, expected_value', [(6, "8"), (0, None)])
def test_get_data_from_db_and_cache(key: int, expected_value: any):
        """
        Test the returned value from the db and memory based on the key provided
        """
        api_response = requests.get(get_api_url, {'key': key})
        db_response = get_from_db(key)
        assert api_response.json().get('value') == expected_value
        assert db_response == expected_value