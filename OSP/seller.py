from flask import Blueprint, url_for, redirect, render_template, request
from pymongo import MongoClient
from . import Entities

seller_print = Blueprint('seller', __name__, url_prefix = '/seller')

try:
    mongo = MongoClient("mongodb+srv://rrohit:BestTrio123@cluster0.iwy8x.mongodb.net/test?retryWrites=true&w=majority") 
    db = mongo.test
except Exception as e:
    print(e)

@seller_print.route('/<username>', methods = ['POST', 'GET'])
def SHome(username):
    return render_template('uploaditem.html')
    
@seller_print.route('/<username>/account', methods = ['GET'])
def UserInfo(username):
    userData = db.users.find_one({"username":username})
    buyerData = db.buyers.find_one({"username":username})
    return render_template('account.html', username, buyerDate['history'])

@seller_print.route('/<username>/shopping_cart', methods = ['GET', 'POST'])
def ShoppingCart(username):
    buyerData = db.buyers.find_one({"username":username})
    if request.method == 'GET':
        return render_template('ShoppingCart.html', username = username)
    # elif request.method == 'POST':
