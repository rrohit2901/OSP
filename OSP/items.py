from flask import Blueprint, url_for, redirect, render_template, request
from pymongo import MongoClient
import cloudinary as Cloud
from . import Entities
import json

item_print = Blueprint('items', __name__, url_prefix = '/items')

try:
    mongo = MongoClient("mongodb+srv://rrohit:BestTrio123@cluster0.iwy8x.mongodb.net/test?retryWrites=true&w=majority") 
    db = mongo.test
except Exception as e:
    print(e)

Cloud.config.update = ({
    'cloud_name':'dr9bqxbvl',
    'api_key': '272421966456345',
    'api_secret': '9TNQuB7knqB7ws0j55xsmb-4K_s'
})

@item_print.route('/<itemid>/<session>/<username>', methods = ['POST', 'GET'])
def ItemPage(itemid, session, username):
    item = db.items.find_one({"ItemId":int(itemid)})
    print(item)
    if request.method == 'GET':
        if not session:
            redirect('/')
        Ssession = json.loads(session)
        return render_template('Item.html', item = item, session = session, username = Ssession['username'])
    if request.method == 'POST':
        Ssession = json.loads(session)
        user = Entities.Buyer(db.users.find_one({"username":Ssession['username']}), db.buyers.find_one({"username":Ssession['username']}), db)
        order = {"item":itemid, "qty":1}
        user.AddToCart(order)
        return render_template('Item.html', item = item, session = session, username = Ssession['username'])