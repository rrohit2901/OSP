import random
import string
import cloudinary as Cloud
import smtplib
from pymongo.mongo_client import MongoClient
from email.message import EmailMessage
class Item():
    Id = 0
    def __init__(self, name, category, price, image, age, company, info, seller, weight, db):
        self.name = name
        self.category = category
        self.price = price
        self.image = image
        self.age = age
        self.company = company
        self.info = info
        self.seller = seller
        self.isHeavy = True if weight>500 else False
        self.isVerified = False
        self.city = self.seller.city
        self.db = db
        self.item_id = Item.Id
        Item.Id += 1
        self.db.items.insert_one({
            "name":name,
            "category":category,
            "price":price,
            "image":image,
            "age":age,
            "company":company,
            "info":info,
            "seller":seller.username,
            "isHeavy":1 if self.isHeavy else 0,
            "isVerified":0,
            "city":self.city,
            "ItemId":item_id
        })
    
    def Verify(self):
        self.isVerified = True
        self.db.items.update_one({"ItemId:self.item_id"}, {"$set":{"isVerified":1}})
    
    def GetName(self):
        return self.name
    
    def GetCategory(self):
        return self.category
    
    def GetSeller(self):
        return self.seller
    
    def Getprice(self):
        return self.price
    
    def GetAge(self):
        return self.age

    def IsHeavy(self):
        return self.isHeavy
    
    def IsVerified(self):
        return self.isVerified
    
    def GetImage(self):
        return self.image
    
    def GetCompany(self):
        return self.company


class Order():
    def __init__(self, item, buyer, status):
        self.items = item
        self.status = status
        self.buyer = buyer
        self.quantity = 1
    def IncreaseQty(self, item):
        self.quantity += 1
    def GetItem(self):
        return self.item
    def GetQty(self):
        return self.quantity


class Person():
    def __init__(self, name, email, telephone, address, db):
        self.name = name
        self.email = email
        self.telephone = telephone
        self.address = address
        self.db = db
    def GetName(self):
        return self.name
    def GetEmail(self):
        return self.email
    def GetPhone(self):
        return self.telephone
    def GetAddr(self):
        return self.address

class Manager(Person):
    
    def __init__(self, name, email, telephone, address, gender, DOB, db, username, password = None):
        self.super.__init__(name, email, telephone, address, db)
        self.gender = gender
        self.DOB = DOB
        self.username = username
        self.imId = self.db.managers.count()
        self.bioId = self.db.managres.count()
        if password is not None:
            self.password = password
        else:
            password_length = 10
            self.password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(password_length))
    
    def UploadToDB(self):
        self.db.managers.insert_one({
            "name":self.name, 
            "email":self.email, 
            "telephone":self.telephone, 
            "address":self.address, 
            "gender":self.gender, 
            "DOB":self.DOB, 
            "username":self.username, 
            "password":self.password
        })
    
    def ManageBuyer(self):
        pass

    def ManageSeller(self):
        pass

    def Audit(self):
        pass

    def ManageItem(self):
        pass

    def HelpNego(self):
        pass
    
    def GetDOB(self):
        return self.DOB
    
    def GetimId(self):
        return self.imId
    
    def GetbioId(self):
        return self.bioID

    def GetuserName(self):
        return self.username


class Customer(Person):
    def __init__(self, name, email, telephone, address, city, state, country, db, username, password = None):
        super().__init__(name, email, telephone, address, db)
        self.city = city
        self.state = state
        self.country = country
        self.iD = self.db.users.count()
        self.username = username
        if password is not None:
            self.password = password
        else:
            password_length = 10
            self.password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(password_length))
    
    def Getcity(self):
        return self.city
    
    def GetuserName(self):
        return self.username
    
    def GetId(self):
        return self.iD

    
class Buyer(Customer):
    def __init__(self, user, buyer, db):
        super().__init__(user['name'], user['email'], user['telephone'], user['address'], user['city'], user['state'], user['country'], db, user['username'], user['password'])
        self.buyerId = self.iD
        self.history = buyer['history']
        self.shoppingCart = buyer['shoppingCart']  
    
        
    def UpdateDb(self):
        self.db.buyers.update_one({"username":self.username},{"$set":{"history":self.history, "shoppingCart":self.shoppingCart}})
    
    def AddToCart(self, item):
        self.shoppingCart.append(item)
        self.UpdateDb()
    
    def RemoveFromCart(self, item):
        self.shoppingCart.remove(item)
        self.UpdateDb()

    def Checkout(self):
        # Sharing contact details
        for item in self.shoppingCart:
            seller = self.db.users.find_one({"username":self.db.items.find_one({"ItemId":item['item']})['seller']})
            mail_sender = smtplib.SMTP('smtp.gmail.com', 587)
            mail_sender.starttls()
            mail_sender.login("ospgrp37@gmail.com", "BestTrio123")
            mail = EmailMessage()
            mail['From'] = 'osgrp37@gmail.com'
            mail['To'] = seller['email']
            mail['Subject'] = "Order requested."
            message = "Hi {},\n{} has requested to buy {} through our portal and order to proceed further you are supposed to contact the buyer. The contact details of the buyer are:-\n\t\t\tName - {}\n\t\t\tEmail Id - {}\n\t\t\tMobile number - {}\nRegards\nTeam 37".format(seller['name'], self.name, self.db.items.find_one({"ItemId":item['item']})['name'],self.name, self.email, self.telephone)
            mail.set_content(message)
            mail_sender.send_message(mail)
            mail_sender.quit()
            # Updating other things
            order = {
                "item":self.db.items.find_one({"ItemId":item['item']}),
                "buyer":self.username,
                "status":"pending"
            }
            self.history.append(order)
        mail_sender = smtplib.SMTP('smtp.gmail.com', 587)
        mail_sender.starttls()
        mail_sender.login("ospgrp37@gmail.com", "BestTrio123")
        mail = EmailMessage()
        mail['From'] = 'osgrp37@gmail.com'
        mail['To'] = self.email
        mail['Subject'] = "Order details."
        message = "Hi\ {},\n\
            You requested to buy following items through our portal and order to proceed further you are supposed to contact the buyer of corresponding products.\
            The contact details of the sellers are:-\n\
            ".format(self.name)
        for item in self.shoppingCart:
            seller = self.db.users.find_one({"username":self.db.items.find_one({"ItemId":item['item']})['seller']})
            message += "-- Name of item = {}\n   Name of seller = {}\n   Email of seller = {}\n   Mobile number of seller = {}\n".format(self.db.items.find_one({"ItemId":item['item']})['name'], seller['name'], seller['email'], seller['telephone'])
        mail.set_content(message)
        mail_sender.send_message(mail)
        mail_sender.quit()
        self.shoppingCart.clear()
        self.UpdateDb()
    
    def InitiateNegotiation(self):
        pass

    def GetHistory(self):
        return self.history

    def AddToDB(self):
        self.db.users.insert_one({
            "name":self.name, 
            "email":self.email, 
            "telephone":self.telephone, 
            "address":self.address, 
            "city":self.city,
            "state":self.state,
            "country":self.country,
            "Id":self.iD,
            "username":self.username,
            "password":self.password
        })
        self.db.buyers.insert_one({
            "username":self.username,
            "shoppingCart":self.shoppingCart,
            "history":self.history
        })

class Seller(Customer):
    def __init__(self, name, email, telephone, address, db, username, password = None):
        self.super.__init__(name, email, telephone, address, db, username, password)
        self.sellerId = self.iD
        self.items = []

    def UpdateDb(self):
        self.db.users.update_one({"username":self.username},{"$set":{"items":self.items}})

    def UplaodItem(self, item):
        pass

    def Negotiate(self):
        pass
    