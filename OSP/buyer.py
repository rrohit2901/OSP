from flask import Blueprint, url_for, redirect, render_template, request
from pymongo import MongoClient
from . import Entities

buyer_print = Blueprint('buyer', __name__, url_prefix = '/buyer')

try:
    mongo = MongoClient("mongodb+srv://rrohit:BestTrio123@cluster0.iwy8x.mongodb.net/test?retryWrites=true&w=majority") 
    db = mongo.test
except Exception as e:
    print(e)

@buyer_print.route('/<username>', methods = ['POST', 'GET'])
def BHome(username):
    if request.method == 'GET':
        items = dict()
        for item in db.items.find({}):
            if item['category'] in items.keys():
                items[item['category']].append(item)
            else:
                items[item['category']] = []
                items[item['category']].append(item)
        return render_template('Buyer.html', items = items, username = username)
    
    elif request.method == 'POST':
        if request.form.get('search_button'):
            searchQuery = request.form['query']
            items = None
            if searchType=='Name':
                items = db.getCollection('items').find({"name":searchQuery}).limit(3)
            return "##"
        else:
            return "%%"
    
@buyer_print.route('/<username>/account', methods = ['GET'])
def UserInfo(username):
    userData = db.users.find_one({"username":username})
    buyerData = db.buyers.find_one({"username":username})
    return render_template('account.html', username, buyerDate['history'])

@buyer_print.route('/<username>/shopping_cart', methods = ['GET', 'POST'])
def ShoppingCart(username):
    buyerData = db.buyers.find_one({"username":username})
    if request.method == 'GET':
        return render_template('ShoppingCart.html', username = username)
    # elif request.method == 'POST':
