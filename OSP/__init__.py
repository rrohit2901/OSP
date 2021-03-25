import os
import re
import string
import random
import smtplib
from pymongo import MongoClient
from flask import Flask, request, render_template, url_for, flash, redirect


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    try:
        mongo = MongoClient("mongodb+srv://rrohit:Nikita123@cluster0.iwy8x.mongodb.net/test?retryWrites=true&w=majority") 
        db = mongo.test
    except Exception as e:
        print(e)
    

    @app.route('/buyer')
    def buyer():
        return redirect('/buyer/login')

    @app.route('/buyer/login', methods = ['POST', 'GET'])
    def loginAsBuyer():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            error = None

            if not db.users.find_one({"username":username}):
                error = 'Invalid username'
            elif db.users.find_one({"username":username})['password']!=password:
                error = 'Invalid password'
            
            if error==None:
                print(db.users.find_one({"username":username}))
                return "$$$"

            flash(error)
        return render_template('login.html')

    @app.route('/seller')
    def seller():
        return redirect('/seller/login')

    @app.route('/seller/login', methods = ['POST', 'GET'])
    def loginAsSeller():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            error = None

            if not db.users.find_one({"username":username}):
                error = 'Invalid username'
            elif db.users.find_one({"username":username})['password']!=password:
                error = 'Invalid password'
            
            if error==None:
                print(db.users.find_one({"username":username}))
                return "%%%"

            flash(error)
        return render_template('login.html')

    @app.route('/')
    def home():
        return redirect('/home')

    @app.route('/home', methods = ['GET','POST'])
    def register():
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']
            address = request.form['address']
            mobile_number = request.form['mobile_number']
            
            # Error in the validation of form
            error = None

            if not name:
                error = 'Name of user is required'
            elif not email:
                error = 'Email is required'
            elif not city:
                error = 'City is required'
            elif not state:
                error = 'State is required'
            elif not country:
                error = 'Country is required'
            elif not address:
                error = 'Address is required'
            elif db.users.find_one({"email":email}):
                error = 'Email is already registered'
            elif db.users.find_one({"mobile_number":mobile_number}):
                error = 'Mobile number is already registered'
            elif not mobile_number:
                error = 'Mobile Number is required'
            elif not re.search(regex,email):
                error = 'Email ID not valid'
            
            if error is None:
                password_length = 10
                username = email.split('@')[0]
                password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(password_length))
                user = {"email":email, "name":name, "username":username, "address":address, "password":password, "mobile_number":mobile_number, "city":city, "state":state, "country":country}
                print(user)
                try:
                    dbResponse = db.users.insert_one(user)
                    mail_sender = smtplib.SMTP('smtp.gmail.com', 587)
                    mail_sender.starttls()
                    mail_sender.login("ospgrp37@gmail.com", "BestTrio123")
                    message = "Hi {},\nWelcome to the online sales portal.\n\nYour login credentials are:-\n\tusername - {}\n\tpassword - {}\n\nHope you enjoy shopping with us.\nRegards,\nTeam 37.".format(name, username, password)
                    mail_sender.sendmail("ospgroup37@gmail.com", email, message)
                    mail_sender.quit()
                except Exception as e:
                    print(e)
                print(url_for('sec'))
                return render_template('register.html')

            flash(error)
        return render_template('register.html')

        

    
    return app