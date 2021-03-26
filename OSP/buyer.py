from flask import Blueprint, url_for, redirect, render_template

buyer_print = Blueprint('buyer', __name__, url_prefix = '/buyer')

@buyer_print.route('/<username>', methods = ['POST', 'GET'])
def BHome(username):
    if request.method == 'GET':
        items = db.getCollection('items').find({}).limit(3)
        return render_template('buyer_search.html', items, username)
    
    elif request.method == 'POST':
        searchType = request.form['type']
        searchQuery = request.form['query']
        items = None
        if searchType=='Category':
            items = db.getCollection('items').find({"category":searchQuery}).limit(3)
        elif searchType=='Name':
            items = db.getCollection('items').find({"name":searchQuery}).limit(3)
        return render_template('buyer_search.html', items, username)
    
@buyer_print.route('/<username>/account', methods = ['GET'])
def UserInfo(username):
    userData = db.users.find_one({"username":username})
    buyerData = db.buyers.find_one({"username":username})
