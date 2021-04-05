from flask import Blueprint, url_for, redirect, render_template, request
from pymongo import MongoClient
import cloudinary as Cloud
import cloudinary.uploader
import smtplib
from email.message import EmailMessage
from . import Entities
import json

seller_print = Blueprint('seller', __name__, url_prefix = '/seller')

try:
    mongo = MongoClient("mongodb+srv://rrohit:BestTrio123@cluster0.iwy8x.mongodb.net/test?retryWrites=true&w=majority") 
    db = mongo.test
except Exception as e:
    print(e)

Cloud.config(
    cloud_name = 'dr9bqxbvl',
    api_key = '272421966456345',
    api_secret = '9TNQuB7knqB7ws0j55xsmb-4K_s'
)

@seller_print.route('/<username>/<session>', methods = ['POST', 'GET'])
def SHome(username, session = None):
    if session is None:
        redirect('/login')

    userdata = db.users.find_one({'username':username})
    sellerData = db.sellers.find_one({"username":username})


    items = []
    for item in db.items.find({}):
        if item['seller'] == username:
            items.append(item)

    order_list = []
    for order in db.orders.find({}):
        if (order['item']['seller'] == username) and (order['status'] == "pending"):
            order_list.append(order)
    
    if request.method == 'POST':
        if request.form.get('Reject'):
            index = int(request.form['Reject'])-1
            order = db.orders.find_one({'_id':order_list[index]['_id']})
            buyer_username = order['buyer']
            history = db.buyers.find_one({'username':buyer_username})['history']
            history.remove(order)
            order['status'] = "rejected"
            history.append(order)
            db.orders.update_one({'_id':order_list[index]['_id']},{"$set":{'status' : 'Rejected'}})
            db.buyers.update_one({'username':buyer_username}, {"$set":{'history':history}})
            del order_list[index]
            user = db.users.find_one({'username':buyer_username})
            mail_sender = smtplib.SMTP('smtp.gmail.com', 587)
            mail_sender.starttls()
            mail_sender.login("ospgrp37@gmail.com", "BestTrio123")
            mail = EmailMessage()
            mail['From'] = 'osgrp37@gmail.com'
            mail['To'] = user['email']
            mail['Subject'] = "Order requested."
            message = "Hi {},\n{} has Rejected your request to buy item through our portal.\nRegards\nTeam 37".format(user['name'], username)
            mail.set_content(message)
            mail_sender.send_message(mail)
            mail_sender.quit()

        elif request.form.get('Confirm'):
            index = int(request.form['Confirm'])-1
            order = db.orders.find_one({'_id':order_list[index]['_id']})
            buyer_username = order['buyer']
            history = db.buyers.find_one({'username':buyer_username})['history']
            history.remove(order)
            order['status'] = "confirmed"
            history.append(order)
            sItems = db.sellers.find_one({'username':username})['items']
            for item in sItems:
                if item['ItemId']==db.orders.find_one({'_id':order_list[index]['_id']})['item']['ItemId']:
                    sItems.remove(item)
                    break
            db.sellers.update_one({'username':username}, {"$set":{'items':sItems}})
            db.orders.update_one({'_id':order_list[index]['_id']},{"$set":{'status' : 'Confirmed'}})
            db.buyers.update_one({'username':buyer_username}, {"$set":{'history':history}})
            db.items.delete_one({'ItemId':db.orders.find_one({'_id':order_list[index]['_id']})['item']['ItemId']})
            del order_list[index]
            user = db.users.find_one({'username':buyer_username})
            mail_sender = smtplib.SMTP('smtp.gmail.com', 587)
            mail_sender.starttls()
            mail_sender.login("ospgrp37@gmail.com", "BestTrio123")
            mail = EmailMessage()
            mail['From'] = 'osgrp37@gmail.com'
            mail['To'] = user['email']
            mail['Subject'] = "Order requested."
            message = "Hi {},\n{} has confirmed your request to buy item through our portal.\nRegards\nTeam 37".format(user['name'], username)
            mail.set_content(message)
            mail_sender.send_message(mail)
            mail_sender.quit()

        elif request.form.get('Del'):
            id = request.form['Del']
            sItems = db.sellers.find_one({'username':username})['items']
            for item in sItems:
                if item['ItemId']==db.orders.find_one({'_id':order_list[index]['_id']})['item']['ItemId']:
                    sItems.remove(item)
                    break
            db.sellers.update_one({'username':username}, {"$set":{'items':sItems}})
            db.items.delete_one({'ItemId':id})
            for buyer in db.buyers.find({}):
                cart = buyer['shoppingCart']
                history = buyer['history']
                for item in cart:
                    if item['item']==id:
                        cart.remove(item)
                        break
                for item in history:
                    if item['item']['ItemId']==id:
                        history.remove(item)
                        break
                db.buyers.update_one({"username":buyer['username']}, {"$set":{"history":history}})
                db.buyers.update_one({"username":buyer['username']}, {"$set":{"shoppingCart":cart}})
        
        else:
            name = request.form['item_name']
            price = request.form['Price']
            category = request.form['Category']
            company = request.form['Company']
            age = request.form['Age']
            info = request.form['desc']
            path1 = request.form['path1']
            image = open(path1+request.form['image'],"rb")
            image = cloudinary.uploader.upload(image)['url']
            print(image)
            seller = username
            weight = int(request.form['weight'])
            item = Entities.Item(name, category, price, image, age, company, info, seller, weight, db)

    return render_template('Seller.html', userdata = userdata, items = items, order_list = order_list, session = session)
