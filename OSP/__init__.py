import os
import re
import string
import random
import smtplib
from pymongo.mongo_client import MongoClient
from flask import Flask, request, render_template, url_for, flash, redirect
from . import Entities
from . import buyer
from . import items
from . import Manager
from . import seller
from email.message import EmailMessage
import json

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
)

# if test_config is None:
#     # load the instance config, if it exists, when not testing
#     app.config.from_pyfile('config.py', silent=True)
# else:
#     # load the test config if passed in
#     app.config.from_mapping(test_config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

app.register_blueprint(buyer.buyer_print)
app.register_blueprint(items.item_print)
app.register_blueprint(Manager.manager_print)
app.register_blueprint(seller.seller_print)

try:
    mongo = MongoClient("mongodb+srv://rrohit:BestTrio123@cluster0.iwy8x.mongodb.net/test?retryWrites=true&w=majority") 
    db = mongo.test
except Exception as e:
    print(e)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    session = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        error = None

        if not db.users.find_one({"username":username}):
            error = 'Invalid username'
        elif db.users.find_one({"username":username})['password']!=password:
            error = 'Invalid password'
        if error==None:
            session = dict()
            session['username'] = username
            session['status'] = "Active"
            jsession = json.dumps(session)
            if role=="1":
                url = url_for('buyer.BHome', username = username, session = jsession)
                return redirect(url)
            else:
                url = url_for('seller.SHome', username = username, session = jsession)
                return redirect(url)
    return render_template('Signin.html')

@app.route('/')
def home():
    return redirect('/home')

@app.route('/home', methods = ['GET','POST'])
def register():
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if request.method == 'POST':
        user_dict = dict()
        user_dict['name'] = request.form['name']
        user_dict['email'] = request.form['email']
        user_dict['city'] = request.form['city']
        user_dict['state'] = request.form['state']
        user_dict['country'] = request.form['country']
        user_dict['address'] = request.form['address']
        user_dict['mobile_number'] = request.form['mobile_number']
        
        # Error in the validation of form
        error = None

        # if not name:
        #     error = 'Name of user is required'
        # elif not email:
        #     error = 'Email is required'
        # elif not city:
        #     error = 'City is required'
        # elif not state:
        #     error = 'State is required'
        # elif not country:
        #     error = 'Country is required'
        # elif not address:
        #     error = 'Address is required'
        # elif db.users.find_one({"email":email}):
        #     error = 'Email is already registered'
        # elif db.users.find_one({"telephone":telephone}):
        #     error = 'Mobile number is already registered'
        # elif not mobile_number:
        #     error = 'Mobile Number is required'
        # elif not re.search(regex,email):
        #     error = 'Email ID not valid'
        
        print(error)

        if error is None:
            buyer_dict = dict()
            seller_dict = dict()
            password_length = 10
            user_dict['Id'] = db.users.count()
            user_dict['username'] = user_dict['email'].split('@')[0]
            user_dict['password'] = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(password_length))
            buyer_dict['history'] = []
            buyer_dict['shoppingCart'] = []
            seller_dict['items'] = []
            buyer_ins = Entities.Buyer(user_dict, buyer_dict, db)
            seller_ins = Entities.Seller(user_dict, seller_dict, db)
            try:
                buyer_ins.AddToDB()
                seller_ins.AddToDB()
                mail_sender = smtplib.SMTP('smtp.gmail.com', 587)
                mail_sender.starttls()
                mail_sender.login("ospgrp37@gmail.com", "BestTrio123")
                mail = EmailMessage()
                mail['From'] = 'osgrp37@gmail.com'
                mail['To'] = user_dict['email']
                mail['Subject'] = "OSP"
                message = "Hi {},\nWelcome to the OSP.\n\nYour login credentials are:-\n\tusername - {}\n\tpassword - {}\n\n\nRegards,\nTeam 37.".format(user_dict['name'], user_dict['username'], user_dict['password'])
                mail.set_content(message)
                mail_sender.send_message(mail)
                mail_sender.quit()
            except Exception as e:
                print(e)
            return render_template('Register.html')

    return render_template('Register.html')
