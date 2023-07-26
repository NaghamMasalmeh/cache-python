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


def add_data_to_db(data: dict) -> dict:
    """
    Add data to the database
    """
    put_in_db(data['key'], data['value'])



def compare_db_data(actual_data: List[dict], expected_data: List[dict]):
    """
    Compare expected data with data returned from the db
    """
    for i, data in enumerate(actual_data):
        assert data['key'] == expected_data[i]['key']
        assert data['value'] == expected_data[i]['value']


def check_db_data(test_data: List[dict]) -> None:
    """
    Compare expected data with data returned from the db
    """
    result = collection.find({})
    compare_db_data(list(result), test_data)


def test_add_data_to_db():
    """
    Test adding data to the db and memory and check the response with the expected data
    """
    for data in test_data:
        add_data_to_db(data)
    check_db_data(test_data)


def test_evict_item_in_db():
    """
    Test the LRU algorithm by removing the LRU item from the cache
    """
    add_data_to_db(new_data)
    check_db_data(test_data_with_evicted_value)


def test_update_item_in_db():
    """
    Test Updating item in the db
    """
    add_data_to_db(updated_data)
    check_db_data(test_data_with_updated_value)


@pytest.mark.parametrize('key, expected_value', [(6, "8"), (0, None)])
def test_get_data_from_db(key: int, expected_value: any):
        """
        Test the returned value from the db based on the key provided
        """
        db_response = get_from_db(key)
        assert db_response == expected_value