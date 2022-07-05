from unittest.mock import patch, Mock

import pytest
from dotenv import load_dotenv, find_dotenv

from todo_app.app import create_app

@pytest.fixture
def test_environment_vars():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)


@pytest.fixture
def client(test_environment_vars):
    with create_app().test_client() as client:
        yield client


@patch('requests.get')
def test_index_page(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists

    response = client.get('/')

    response_html = response.data.decode()
    assert 'My Next Task' in response_html
    assert 'My In Progress Task' in response_html
    assert 'My Completed Task' in response_html


TODO_LIST_ID = '4db8eac66a17902384424114'
DOING_LIST_ID = 'c1a6155629848335595f4244'
DONE_LIST_ID = 'd71a203ae9a9861932cb0d57'

TODO_ITEM_ID = '1a3aed73b1b8874546225f83'
DOING_ITEM_ID = 'e8f4491c7b333fb2852206ea'
DONE_ITEM_ID = '11cc569ac7340679a0b922a7'

sample_trello_lists_response = [
    {
        "id": TODO_LIST_ID,
        "name": "To Do",
        "cards": [
            {
                "id": TODO_ITEM_ID,
                "dateLastActivity": "2022-06-10T15:48:26.091Z",
                "name": "My Next Task"
            }
        ]
    },
    {
        "id": DOING_LIST_ID,
        "name": "Doing",
        "cards": [
            {
                "id": DOING_ITEM_ID,
                "dateLastActivity": "2022-06-10T15:48:26.091Z",
                "name": "My In Progress Task"
            }
        ]
    },
    {
        "id": DONE_LIST_ID,
        "name": "Done",
        "cards": [
            {
                "id": DONE_ITEM_ID,
                "dateLastActivity": "2022-06-10T15:48:26.091Z",
                "name": "My Completed Task"
            }
        ]
    }
]

def mock_get_lists(url, params):
    if url == 'https://api.trello.com/1/boards/abcd1234/lists':
        response = Mock(ok=True)
        response.json.return_value = sample_trello_lists_response
        return response

    return None
