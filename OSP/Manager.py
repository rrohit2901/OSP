from flask import Blueprint, url_for, redirect, render_template, request
from pymongo import MongoClient
import cloudinary as Cloud
from . import Entities
import json
import re
import random
import string
import smtplib
from email.message import EmailMessage
import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


manager_print = Blueprint('manager', __name__, url_prefix = '/manager', template_folder = 'Manager/xtreme-html/ltr')

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


@manager_print.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

@manager_print.route('/login', methods = ['GET', 'POST'])
def login():
    session = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        if not db.managers.find_one({"username":username}):
            error = 'Invalid username'
        elif db.managers.find_one({"username":username})['password']!=password:
            error = 'Invalid password'
        print(error)
        if error==None:
            session = dict()
            session['username'] = username
            session['status'] = "Active"
            jsession = json.dumps(session)
            return redirect(url_for('manager.MHome', username = username, session = jsession))
    return render_template('MSignin.html')

@manager_print.route('/')
def home():
    return redirect('/register')

@manager_print.route('/register', methods = ['GET','POST'])
def register():
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        gender = request.form['gender']
        address = request.form['address']
        telephone = request.form['mobile_number']
        DOB = request.form['DOB']
        
        # Error in the validation of form
        error = None

        if not name:
            error = 'Name of user is required'
        elif not email:
            error = 'Email is required'
        elif not address:
            error = 'Address is required'
        elif db.managers.find_one({"email":email}):
            error = 'Email is already registered'
        elif db.managers.find_one({"telephone":telephone}):
            error = 'Mobile number is already registered'
        elif not telephone:
            error = 'Mobile Number is required'
        elif not re.search(regex,email):
            error = 'Email ID not valid'
        
        print(error)

        if error is None:
            password_length = 10
            username = email.split('@')[0]
            password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(password_length))
            manager_ins = Entities.Manager(name, email, telephone, address, gender, DOB, db, username, password)
            try:
                manager_ins.UploadToDB()
                mail_sender = smtplib.SMTP('smtp.gmail.com', 587)
                mail_sender.starttls()
                mail_sender.login("ospgrp37@gmail.com", "BestTrio123")
                mail = EmailMessage()
                mail['From'] = 'osgrp37@gmail.com'
                mail['To'] = email
                mail['Subject'] = "OSP"
                message = "Hi {},\nWelcome to the OSP.\n\nYour login credentials are:-\n\tusername - {}\n\tpassword - {}\n\n\nRegards,\nTeam 37.".format(name, username, password)
                mail.set_content(message)
                mail_sender.send_message(mail)
                mail_sender.quit()
            except Exception as e:
                print(e)
    return render_template('MRegister.html')

@manager_print.route('/<username>/<session>', methods = ['POST', 'GET'])
def MHome(username, session):
    if request.method == 'GET':
        manager_obj = db.managers.find_one({"username":username})
        print(manager_obj)
        users = []
        for user in db.users.find({}):
            users.append(user)
        print(users)
        categories = []
        items = []
        for item in db.items.find({}):
            items.append(item)
            if not item['category'] in categories:
                categories.append(item['category'])
        tasks = []
        for item in db.negotiations.find({}):
            tasks.append(item)
        return render_template('Manager.html', username = username, session = session, manager_obj = manager_obj, users = users, items = items, orders = 5, categories = categories)
    elif request.method == 'POST':
        if request.form.get('delItem'):
            id = int(request.form['delItem'])
            db.items.delete_one({"ItemId":id})
            manager_obj = db.managers.find_one({"username":username})
            print(manager_obj)
            users = []
            for user in db.users.find({}):
                users.append(user)
            print(users)
            categories = []
            items = []
            for item in db.items.find({}):
                items.append(item)
                if not item['category'] in categories:
                    categories.append(item['category'])
            tasks = []
            for item in db.negotiations.find({}):
                tasks.append(item)
            return render_template('Manager.html', username = username, session = session, manager_obj = manager_obj, users = users, items = items, orders = 5, categories = categories)
        elif request.form.get('verify'):
            id = int(request.form['verify'])
            db.items.update_one({"ItemId":str(id)}, {"$set":{"isVerified":str(1)}})
            manager_obj = db.managers.find_one({"username":username})
            print(manager_obj)
            users = []
            for user in db.users.find({}):
                users.append(user)
            print(users)
            categories = []
            items = []
            for item in db.items.find({}):
                items.append(item)
                if not item['category'] in categories:
                    categories.append(item['category'])
            tasks = []
            for item in db.negotiations.find({}):
                tasks.append(item)
            return render_template('Manager.html', username = username, session = session, manager_obj = manager_obj, users = users, items = items, orders = 5, categories = categories)
        elif request.form.get('accn'):
            id = int(request.form['accn'])
            print(id)
            username = db.users.find_one({"Id":id})['username']
            user_inf = db.users.find_one({'username':username})
            buyer_inf = db.buyers.find_one({'username': username})
            try:
                user = Entities.Buyer(user_inf, buyer_inf, db)
            except Exception as e:
                print(e)
            userdata = db.users.find_one({'username':username})
            return render_template('MyAccount.html', userdata = userdata, history = buyer_inf['history'], session = session)
        elif request.form.get('del'):
            id = int(request.form['del'])
            db.users.delete_one({"Id":id})
            manager_obj = db.managers.find_one({"username":username})
            print(manager_obj)
            users = []
            for user in db.users.find({}):
                users.append(user)
            print(users)
            categories = []
            items = []
            for item in db.items.find({}):
                items.append(item)
                if not item['category'] in categories:
                    categories.append(item['category'])
            tasks = []
            for item in db.negotiations.find({}):
                tasks.append(item)
            return render_template('Manager.html', username = username, session = session, manager_obj = manager_obj, users = users, items = items, orders = 5, categories = categories)
        elif request.form.get('accn_1'):
            id = int(request.form['accn_1'])
            print(id)
            username = db.users.find_one({"Id":id})['username']
            user_inf = db.users.find_one({'username':username})
            buyer_inf = db.buyers.find_one({'username': username})
            try:
                user = Entities.Buyer(user_inf, buyer_inf, db)
            except Exception as e:
                print(e)
            userdata = db.users.find_one({'username':username})
            return render_template('MyAccount.html', userdata = userdata, history = buyer_inf['history'], session = session)
        elif request.form.get('del_1'):
            id = int(request.form['del_1'])
            db.users.delete_one({"Id":id})
            manager_obj = db.managers.find_one({"username":username})
            print(manager_obj)
            users = []
            for user in db.users.find({}):
                users.append(user)
            print(users)
            categories = []
            items = []
            for item in db.items.find({}):
                items.append(item)
                if not item['category'] in categories:
                    categories.append(item['category'])
            tasks = []
            for item in db.negotiations.find({}):
                tasks.append(item)
            return render_template('Manager.html', username = username, session = session, manager_obj = manager_obj, users = users, items = items, orders = 5, categories = categories)
        elif request.form.get('categoryChange'):
            category = request.form['categoryChange'].split('_')[0]
            id = int(request.form['categoryChange'].split('_')[1])
            db.items.update_one({"ItemId":id}, {"$set":{"category":category}})
            manager_obj = db.managers.find_one({"username":username})
            print(manager_obj)
            users = []
            for user in db.users.find({}):
                users.append(user)
            print(users)
            categories = []
            items = []
            for item in db.items.find({}):
                items.append(item)
                if not item['category'] in categories:
                    categories.append(item['category'])
            tasks = []
            for item in db.negotiations.find({}):
                tasks.append(item)
            return render_template('Manager.html', username = username, session = session, manager_obj = manager_obj, users = users, items = items, orders = 5, categories = categories)            
        elif request.form.get('signout'):
            return redirect(url_for('manager.login'))
        elif request.form.get('itemPage'):
            Ssession = json.loads(session)
            id = int(request.form['itemPage'])
            item = db.items.find_one({"ItemId":id})
            print(item)
            return render_template('Item.html', item = item, session = session, username = Ssession['username'])