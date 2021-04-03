from flask import Blueprint, url_for, redirect, render_template, request
from pymongo import MongoClient
import cloudinary as Cloud
from . import Entities
import json

buyer_print = Blueprint('buyer', __name__, url_prefix = '/buyer')

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

@buyer_print.route('/<username>/<session>', methods = ['POST', 'GET'])
def BHome(username, session = None):
    if session is None:
        redirect('/login')
    Ssession = json.loads(session)
    if not session or Ssession['username']!=username:
        redirect("/")
    if request.method == 'GET':
        items = dict()
        items.clear()
        for item in db.items.find({}):
            if item['category'] in items.keys():
                items[item['category']].append(item)
            else:
                items[item['category']] = []
                items[item['category']].append(item)
        return render_template('Buyer.html', items = items, username = username, session = session)
    
    elif request.method == 'POST':
        if request.form.get('search_button'):
            searchQuery = request.form['query']
            items = db.items.find({"name":searchQuery}).limit(3)
            print(items[0]['name'])
            return "##"
        elif request.form.get('AddToCart'):
            id = request.form['AddToCart']
            for order in db.buyers.find_one({"username":username})['shoppingCart']:
                if order['item']==str(id):
                    items = dict()
                    items.clear()
                    for item in db.items.find({}):
                        if item['category'] in items.keys():
                            items[item['category']].append(item)
                        else:
                            items[item['category']] = []
                            items[item['category']].append(item)
                    return render_template('Buyer.html', items = items, username = username, session = session)
            user_inf = db.users.find_one({'username':username})
            buyer_inf = db.buyers.find_one({'username': username})
            try:
                user = Entities.Buyer(user_inf, buyer_inf, db)
            except Exception as e:
                print(e)
            order = {"item":id, "qty":1}
            user.AddToCart(order)
            items = dict()
            items.clear()
            for item in db.items.find({}):
                if item['category'] in items.keys():
                    items[item['category']].append(item)
                else:
                    items[item['category']] = []
                    items[item['category']].append(item)
            return render_template('Buyer.html', items = items, username = username, session = session)
    
@buyer_print.route('/<username>/account/<session>', methods = ['GET'])
def UserInfo(username, session = None):
    userdata = db.users.find_one({'username':username})
    buyerData = db.buyers.find_one({"username":username})
    print(buyerData)
    return render_template('MyAccount.html', userdata = userdata, history = buyerData['history'], session = session)

@buyer_print.route('/<username>/shopping_cart/<session>', methods = ['GET', 'POST'])
def ShoppingCart(username, session = None):
    buyerData = db.buyers.find_one({"username":username})
    if request.method == 'GET':
        items = []
        qtyD = dict()
        sum = 0
        for order in buyerData['shoppingCart']:
            items.append(db.items.find_one({"ItemId":order['item']}))
            qtyD[order['item']] = order['qty']
            sum += int(db.items.find_one({"ItemId":order['item']})['price']) * int(order['qty'])
        return render_template('MyCart.html', username = username, items = items, sum = sum, session = session, qtyD = qtyD)
    elif request.method == 'POST':
        if request.form.get('checkout'):
            user_inf = db.users.find_one({'username':username})
            buyer_inf = db.buyers.find_one({'username': username})
            try:
                user = Entities.Buyer(user_inf, buyer_inf, db)
            except Exception as e:
                print(e)
            user.Checkout()
            userdata = db.users.find_one({'username':username})
            return render_template('MyAccount.html', userdata = userdata, history = buyer_inf['history'], session = session)
        elif request.form.get('qtyc') and request.form['qtyc'].split('_')[0] == 'minus':
            id = int(request.form['qtyc'].split('_')[1])
            print(id)
            items = []
            qtyD = dict()
            sum = 0
            remList = []
            for order in buyerData['shoppingCart']:
                if order['item']==str(id) and order['qty']>0:
                    order['qty'] -= 1
                if order['qty']==0:
                    remList.append(order)
                    continue
                items.append(db.items.find_one({"ItemId":order['item']}))
                qtyD[order['item']] = order['qty']
                sum += int(db.items.find_one({"ItemId":order['item']})['price']) * int(order['qty'])
            for order in remList:
                buyerData['shoppingCart'].remove(order)
            db.buyers.update_one({"username":username},{"$set":{"shoppingCart" : buyerData['shoppingCart']}})
            return render_template('MyCart.html', username = username, items = items, sum = sum, session = session, qtyD = qtyD)
        elif request.form.get('qtyc') and request.form['qtyc'].split('_')[0] == 'plus':
            id = int(request.form['qtyc'].split('_')[1])
            print(id)
            items = []
            qtyD = dict()
            sum = 0
            for order in buyerData['shoppingCart']:
                items.append(db.items.find_one({"ItemId":order['item']}))
                if order['item']==str(id):
                    order['qty'] += 1
                qtyD[order['item']] = order['qty']
                sum += int(db.items.find_one({"ItemId":order['item']})['price']) * int(order['qty'])
            db.buyers.update_one({"username":username},{"$set":{"shoppingCart" : buyerData['shoppingCart']}})
            return render_template('MyCart.html', username = username, items = items, sum = sum, session = session, qtyD = qtyD)
        elif request.form.get('removeItem'):
            id = int(request.form['removeItem'].split('_')[1])
            for order in buyerData['shoppingCart']:
                if order['item']==str(id):
                    buyerData['shoppingCart'].remove(order)
            items = []
            qtyD = dict()
            sum = 0
            for order in buyerData['shoppingCart']:
                items.append(db.items.find_one({"ItemId":order['item']}))
                qtyD[order['item']] = order['qty']
                sum += int(db.items.find_one({"ItemId":order['item']})['price']) * int(order['qty'])
            db.buyers.update_one({"username":username},{"$set":{"shoppingCart" : buyerData['shoppingCart']}})
            return render_template('MyCart.html', username = username, items = items, sum = sum, session = session, qtyD = qtyD)
