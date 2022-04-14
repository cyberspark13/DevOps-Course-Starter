import os
from unicodedata import name
from wsgiref.util import request_uri
from flask import Flask, render_template, request, redirect, session
import requests
from todo_app.flask_config import Config


api_key = os.getenv('TAPI_KEY')
api_token = os.getenv('TAPI_TOKEN')
key = "key=" + api_key
token = "token=" + api_token

app = Flask(__name__)
app.config.from_object(Config())

#Exercise 2

def get_boards():
    #Get all the names and ids of boards associated with api key
    return ("https://api.trello.com/1/members/me/boards?" + key + "&" + token + "&fields=name")

def get_cards(board_id):
    #Get all the cards associated with a board
    return ("https://api.trello.com/1/boards/" + board_id + "/cards?" + key + "&" + token)

def get_board_boardid(board_id):
    #Get the name of a board from the board id
    return ("https://api.trello.com/1/boards/" + board_id + "?" + key + "&" + token + "&fields=name")

def get_board_cardid(card_id):
    #Get the name of a board from the card id
    return ("https://api.trello.com/1/cards/" + card_id + "/board?" + key + "&" + token + "&fields=name")

def get_board_lists(board_id):
    #Get all the lists on a board
    return ("https://api.trello.com/1/boards/" + board_id + "/lists?" + key + "&" + token)

def get_card_cardid(card_id):
    #Get the name and description of a card from the card id
    return ("https://api.trello.com/1/cards/" + card_id + "?" + key + "&" + token + "&fields=name,desc")

def edit_card_list(listid, cardid):
    #edit the list of the card
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
        return ("https://api.trello.com/1/cards?idList=" + self.list + "&name=" + self.name + "&desc=" + self.desc + "&" + key + "&" + token)

@app.route('/')
def trello():
    boards = make_request(get_boards())
    return  render_template('index.html', boards=boards)

@app.route('/list', methods=['POST'])
def list():
    board_id = request.form.get('selected')
    board_name = make_request(get_board_boardid(board_id))
    cards = make_request(get_cards(board_id))
    return  render_template('list.html', cards=cards, name=board_name)

@app.route('/addcard', methods=['POST'])
#Page to input data for new card
def addcard():
    board_id = request.form.get('selected')
    lists = make_request(get_board_lists(board_id))
    board_name = make_request(get_board_boardid(board_id))
    return  render_template('addcard.html', lists=lists, name=board_name)

@app.route('/addcardapi', methods=['POST'])
#Empty page to execute api call to add card
def addcardapi():
    card = Card(request.form.get('selected'), request.form.get('card_name'), request.form.get('card_desc'))
    make_request_post(card.add_card())
    return redirect('/')

@app.route('/editcard', methods=['POST'])
def editcard():
#Page to select new list for card
    card_id = request.form.get('selected')
    session['card_id'] = card_id
    board = make_request(get_board_cardid(card_id))
    lists = make_request(get_board_lists(board.get('id')))
    card = make_request(get_card_cardid(card_id))
    return render_template('editcard.html', lists=lists, card=card, board=board)

@app.route('/editcardapi', methods=['POST'])
def editcardapi():
#Empty page to execute api call to edit card list
    list_id = request.form.get('selected')
    card_id = session.get('card_id')
    make_request_put(edit_card_list(list_id, card_id))
    return redirect('/')