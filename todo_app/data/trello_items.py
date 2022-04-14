import requests
import os

api_key=os.getenv('TKEY')
api_token=os.getenv('TToken')

def get_trello_cards():
    """
    Fetches all cards from the board.

    Returns:
        list: The list of saved items.
    """
    payload={'key':os.getenv('TKEY'), 'token':os.getenv('TTOKEN')}
    r=requests.get('https://api.github.com/boards/62572b6c3d07ac80c538d9d6/lists', params=payload)
    r.json()

def get_boards():
    #Get all the names and ids of boards associated with api key
    key = "key=" + api_key
    token = "token=" + api_token
    return ("https://api.trello.com/1/members/me/boards?" + key + "&" + token + "&fields=name")

def get_cards(board_id):
    #Get all the cards associated with a board
    key = "key=" + api_key
    token = "token=" + api_token
    return ("https://api.trello.com/1/boards/" + board_id + "/cards?" + key + "&" + token)

def get_board_boardid(board_id):
    #Get the name of a board from the board id
    key = "key=" + api_key
    token = "token=" + api_token
    return ("https://api.trello.com/1/boards/" + board_id + "?" + key + "&" + token + "&fields=name")

def get_board_cardid(card_id):
    #Get the name of a board from the card id
    key = "key=" + api_key
    token = "token=" + api_token
    return ("https://api.trello.com/1/cards/" + card_id + "/board?" + key + "&" + token + "&fields=name")

def get_board_lists(board_id):
    #Get all the lists on a board
    key = "key=" + api_key
    token = "token=" + api_token
    return ("https://api.trello.com/1/boards/" + board_id + "/lists?" + key + "&" + token)

def get_card_cardid(card_id):
    #Get the name and description of a card from the card id
    key = "key=" + api_key
    token = "token=" + api_token
    return ("https://api.trello.com/1/cards/" + card_id + "?" + key + "&" + token + "&fields=name,desc")

def edit_card_list(listid, cardid):
    #edit the list of the card
    key = "key=" + api_key
    token = "token=" + api_token
    return ("https://api.trello.com/1/cards/" + cardid + "?idList=" + listid + "&" + key + "&" + token)

def make_request(url):
    #make get requests to api
    response = requests.get(url).json()
    return response

def make_request_post(url):
    #make post requests to api
    response = requests.post(url).json()
    return response

def make_request_put(url):
    #make put requests to api
    response = requests.put(url).json()
    return response

class Card:
    def __init__(self, list, name, desc):
        self.list = list
        self.name = name
        self.desc = desc

    def add_card(self):
        #add a new card to a list
        key = "key=" + api_key
        token = "token=" + api_token
        return ("https://api.trello.com/1/cards?idList=" + self.list + "&name=" + self.name + "&desc=" + self.desc + "&" + key + "&" + token)
