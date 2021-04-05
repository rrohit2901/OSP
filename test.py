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
            "ItemId":self.item_id
        })
    
    def Verify(self):
        self.isVerified = True
        self.db.items.update_one({"ItemId":self.item_id}, {"$set":{"isVerified":True}})
    
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

    def UnitTest(self):
        print("name = " + self.GetName())
        print("Category = " + self.GetCategory())
        print("Seller = " + (self.GetSeller()).GetuserName())
        print("price = " + str(self.Getprice()))
        print("age = " + str(self.GetAge()))
        print("isVerified = " + str(self.IsVerified()))
        print("company = " + self.GetCompany())
        print("isHeavy = " + str(self.IsHeavy()))

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
    def __init__(self, name, email, mobile_number, address, db):
        self.name = name
        self.email = email
        self.telephone = mobile_number
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
    
    def __init__(self, name, email, mobile_number, address, gender, DOB, db, username, password = None):
        super().__init__(name, email, mobile_number, address, db)
        self.gender = gender
        self.DOB = DOB
        self.username = username
        self.imId = self.db.managers.count()
        self.bioId = self.db.managers.count()
        if password is not None:
            self.password = password
        else:
            password_length = 10
            self.password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(password_length))
    
    def UploadToDB(self):
        self.db.managers.insert_one({
            "name":self.name, 
            "email":self.email, 
            "mobile_number":self.telephone, 
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
        return self.bioId

    def GetuserName(self):
        return self.username

    def UnitTest(self):
        print("name = " + self.GetName())
        print("DOB = " + self.GetDOB())
        print("imID = " + str(self.GetimId()))
        print("bioID = " + str(self.GetbioId()))
        print("username = " + self.GetuserName())
        print("email = " + self.GetEmail())
        print("telephone = " + self.GetPhone())
        print("addr = " + self.GetAddr())

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

    def  Getpassword(self):
        return self.password
    
class Buyer(Customer):
    def __init__(self, user, buyer, db):
        super().__init__(user['name'], user['email'], user['mobile_number'], user['address'], user['city'], user['state'], user['country'], db, user['username'], user['password'])
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
            self.db.orders.insert_one(order)
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
            message += "-- Name of item = {}\n   Name of seller = {}\n   Email of seller = {}\n   Mobile number of seller = {}\n".format(self.db.items.find_one({"ItemId":item['item']})['name'], seller['name'], seller['email'], seller['mobile_number'])
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
            "mobile_number":self.telephone, 
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

    def UnitTest(self):
        print("name = " + self.GetName())
        print("email = " + self.GetEmail())
        print("telephone = " + self.GetPhone())
        print("addr = " + self.GetAddr())
        print("username = " + self.GetuserName())
        print("password = " + self.Getpassword())
        
class Seller(Customer):
    def __init__(self, user, seller, db):
        super().__init__(user['name'], user['email'], user['mobile_number'], user['address'], user['city'], user['state'], user['country'], db, user['username'], user['password'])
        self.sellerId = self.iD
        #items->item id of the item
        self.items = seller['items']    

    def UpdateDb(self):
        self.db.users.update_one({"username":self.username},{"$set":{"items":self.items}})

    def UplaodItem(self, item):
        self.items.append(item.item_id)
        self.UpdateDb()


    def Negotiate(self):
        pass

    def AddToDB(self):
        '''
        self.db.users.insert_one({
            "name":self.name, 
            "email":self.email, 
            "mobile_number":self.mobile_number, 
            "address":self.address, 
            "city":self.city,
            "Id":self.iD,
            "username":self.username,
            "password":self.password
        })
        '''
        self.db.sellers.insert_one({
            "username":self.username,
            "items":self.items
        })

    def DeleteItem(self, item):
        self.db.items.delete_one(item)
        self.items.remove(item.item_id)
        self.UpdateDb()

    def UnitTest(self):
        print("name = " + self.GetName())
        print("email = " + self.GetEmail())
        print("telephone = " + self.GetPhone())
        print("addr = " + self.GetAddr())
        print("username = " + self.GetuserName())
        print("password = " + self.Getpassword())
        

if __name__ == '__main__':

    try:
        mongo = MongoClient("mongodb+srv://rrohit:BestTrio123@cluster0.iwy8x.mongodb.net/test?retryWrites=true&w=majority") 
        db = mongo.test
    except Exception as e:
        print(e)

    ######### BUYER ###########
    print("######### BUYER #########")
    user_dict = dict()
    user_dict['name'] = "Ishan Goel"
    user_dict['email'] = "ishangoel@gmail.com"
    user_dict['city'] = "Kharagpur"
    user_dict['state'] = "West Bengal"
    user_dict['country'] = "India"
    user_dict['address'] = "LBS hall of residence, IIT KGP"
    user_dict['mobile_number'] = "7456822356"
    user_dict['Id'] = db.users.count()
    user_dict['username'] = "ishangoel"
    user_dict['password'] = "SDBFKJSBF"

    buyer_dict = dict()
    buyer_dict['history'] = []
    buyer_dict['shoppingCart'] = []

    buyer_case1 = Buyer(user_dict, buyer_dict, db=db)
    buyer_case1.UnitTest()

    user_dict.pop('name')
    try:
        buyer_case2 = Buyer(user_dict, buyer_dict, db=db)  
    except Exception as e:
        print(e)

    user_dict['name'] = "Ishan Goel"
    buyer_case3_1 = Buyer(user_dict, buyer_dict, db=db)
    buyer_case3_1.AddToDB()
    buyer_case3_2 = Buyer(user_dict, buyer_dict, db=db)
    buyer_case3_2.AddToDB()
    buyer_case3_3 = Buyer(user_dict, buyer_dict, db=db)
    buyer_case3_3.AddToDB()
    buyer_case3_4 = Buyer(user_dict, buyer_dict, db=db)
    buyer_case3_4.AddToDB()
    buyer_case3_5 = Buyer(user_dict, buyer_dict, db=db)
    buyer_case3_5.AddToDB()
    print("id1 = " + str(buyer_case3_1.GetId()))
    print("id2 = " + str(buyer_case3_2.GetId()))
    print("id3 = " + str(buyer_case3_3.GetId()))
    print("id4 = " + str(buyer_case3_4.GetId()))
    print("id5 = " + str(buyer_case3_5.GetId()))

    user_dict.pop('email')
    try:
        buyer_case4 = Buyer(user_dict, buyer_dict, db=db)  
    except Exception as e:
        print(e)

    ###########################

    ######### BUYER FUNCTIONS ###########


    user_dict = dict()
    user_dict['name'] = "Rohit Raj"
    user_dict['email'] = "rrohit2901@gmail.com"
    user_dict['city'] = "Kharagpur"
    user_dict['state'] = "West Bengal"
    user_dict['country'] = "India"
    user_dict['address'] = "LBS hall of residence, IIT KGP"
    user_dict['mobile_number'] = "7456822356"
    user_dict['Id'] = db.users.count()
    user_dict['username'] = "rrohit2901"
    user_dict['password'] = "SDBFKJSBF"

    seller_dict = dict()
    seller_dict['items'] = []

    buyer_func_case1 = Buyer(user_dict, buyer_dict, db=db)
    buyer_func_case1.AddToDB()
    print(db.users.find_one({'username':user_dict['username']})==None)

    rrohit2901 = Seller(user_dict, seller_dict, db=db)
    item_case1 = Item(name = "Samsung A50", category = "Accessories", price = 5000, 
        image = "https://drive.google.com/drive/u/0/folders/16tcq403pEZLDSzWEShUR2AxwKDqWTYWY", 
        age = 1, company = "Samsung", info = "Nbshbsebfebfejdfjew.asbdfkjbesbfewbf.akejbfkejbs.", 
        seller = rrohit2901, weight = 0.5, db = db)
    buyer_func_case2 = buyer_func_case1
    buyer_func_case2.AddToCart({"item":item_case1.item_id})
    print(True if {"item":item_case1.item_id} in buyer_func_case2.shoppingCart else False)
    buyer_func_case2.Checkout()
    print(True if len(buyer_func_case2.shoppingCart)==0 else False)
    
    print("Checkout can't be called with empty shopping cart")


    #####################################

    ######### SELLER ###########
    print("######### SELLER #########")

    user_dict = dict()
    user_dict['name'] = "Ishan Goel"
    user_dict['email'] = "ishangoel@gmail.com"
    user_dict['city'] = "Kharagpur"
    user_dict['state'] = "West Bengal"
    user_dict['country'] = "India"
    user_dict['address'] = "LBS hall of residence, IIT KGP"
    user_dict['mobile_number'] = "7456822356"
    user_dict['Id'] = db.users.count()
    user_dict['username'] = "ishangoel"
    user_dict['password'] = "SDBFKJSBF"

    seller_dict = dict()
    seller_dict['items'] = []

    seller_case1 = Seller(user_dict, seller_dict, db=db)
    seller_case1.UnitTest()

    user_dict.pop('name')
    try:
        seller_case2 = Seller(user_dict, seller_dict, db=db)
    except Exception as e:
        print(e)

    user_dict['name'] = "Ishan Goel"
    seller_case3_1 = Seller(user_dict, seller_dict, db=db)
    seller_case3_2 = Seller(user_dict, seller_dict, db=db)
    seller_case3_3 = Seller(user_dict, seller_dict, db=db)
    seller_case3_4 = Seller(user_dict, seller_dict, db=db)
    seller_case3_5 = Seller(user_dict, seller_dict, db=db)
    print("id1 = " + str(buyer_case3_1.GetId()))
    print("id2 = " + str(buyer_case3_2.GetId()))
    print("id3 = " + str(buyer_case3_3.GetId()))
    print("id4 = " + str(buyer_case3_4.GetId()))
    print("id5 = " + str(buyer_case3_5.GetId()))

    user_dict.pop('email')
    try:
        seller_case4 = Seller(user_dict, seller_dict, db=db)
    except Exception as e:
        print(e)

    ###########################

    ######### MANAGER ###########
    print("######### MANAGER #########")

    manager_case1 = Manager(name="Rohit Raj", email="rrohit2901@gmail.com", mobile_number="7479125689", 
        address="Nehru Hall of residence, IIT KGP", gender="male", DOB="29/01/2001", db=db, username="rrohit2901",
        password = "HJVJHD23")
    manager_case1.UnitTest()

    manager_case2 = Manager(name="Rohit Raj", email="rrohit2901@gmail.com", mobile_number="7479125689", 
        address="Nehru Hall of residence, IIT KGP", gender="male", DOB="29/01/2001", db=db, username="rrohit2901",
        password = "HJVJHD23")
    manager_case2.UploadToDB()
    print("True")

    manager_case3 = Manager(name="Rohit Raj", email="rrohit2901@gmail.com", mobile_number="7479125689", 
        address="Nehru Hall of residence, IIT KGP", gender="male", DOB="29/01/2001", db=db, username="rrohit2901",
        password = "HJVJHD23")

    ##############################

    ######### ITEM #########
    print("######### ITEM #########")
    user_dict = dict()
    user_dict['name'] = "Rohit Raj"
    user_dict['email'] = "rrohit2901@gmail.com"
    user_dict['city'] = "Kharagpur"
    user_dict['state'] = "West Bengal"
    user_dict['country'] = "India"
    user_dict['address'] = "LBS hall of residence, IIT KGP"
    user_dict['mobile_number'] = "7456822356"
    user_dict['Id'] = db.users.count()
    user_dict['username'] = "rrohit2901"
    user_dict['password'] = "SDBFKJSBF"

    seller_dict = dict()
    seller_dict['items'] = []

    rrohit2901 = Seller(user_dict, seller_dict, db=db)
    item_case1 = Item(name = "Samsung A50", category = "Accessories", price = 5000, 
        image = "https://drive.google.com/drive/u/0/folders/16tcq403pEZLDSzWEShUR2AxwKDqWTYWY", 
        age = 1, company = "Samsung", info = "Nbshbsebfebfejdfjew.asbdfkjbesbfewbf.akejbfkejbs.", 
        seller = rrohit2901, weight = 0.5, db = db)
    item_case1.UnitTest()
    
    item_case2 = item_case1
    item_case2.Verify()
    print(item_case2.IsVerified())

    try:
        item_case3 = Item(category = "Accessories", price = 5000, 
        image = "https://drive.google.com/drive/u/0/folders/16tcq403pEZLDSzWEShUR2AxwKDqWTYWY", 
        age = 1, company = "Samsung", info = "Nbshbsebfebfejdfjew.asbdfkjbesbfewbf.akejbfkejbs.", 
        seller = rrohit2901, weight = 0.5, db = db)
    except Exception as e:
        print(e)

    try:
        item_case4 = Item(name = "Samsung A50", category = "Accessories",
        image = "https://drive.google.com/drive/u/0/folders/16tcq403pEZLDSzWEShUR2AxwKDqWTYWY", 
        age = 1, company = "Samsung", info = "Nbshbsebfebfejdfjew.asbdfkjbesbfewbf.akejbfkejbs.", 
        seller = rrohit2901, weight = 0.5, db = db)
    except Exception as e:
        print(e)
    

    ########################

        ######### SELLER FUNCTIONS ###########
    print("######### SELLER FUNCTIONS #########")

    user_dict = dict()
    user_dict['name'] = "Ishan Goel"
    user_dict['email'] = "ishangoel@gmail.com"
    user_dict['city'] = "Kharagpur"
    user_dict['state'] = "West Bengal"
    user_dict['country'] = "India"
    user_dict['address'] = "LBS hall of residence, IIT KGP"
    user_dict['mobile_number'] = "7456822356"
    user_dict['Id'] = db.users.count()
    user_dict['username'] = "ishangoel"
    user_dict['password'] = "SDBFKJSBF"

    seller_dict = dict()
    seller_dict['items'] = []

    seller_fun_case1 = Seller(user_dict, seller_dict, db=db)
    seller_fun_case1.AddToDB()
    if db.sellers.find_one({'username': user_dict['username']}) is not None:
        print("True")
    else:
        print("False")

    seller_fun_case2 = seller_fun_case1
    seller_fun_case2.UplaodItem(item_case1)
    if db.items.find_one({"ItemId":item_case1.item_id}) is None:
        print("False")
    else:
        print("True")
    try:
        seller_fun_case2.DeleteItem(item_case1)
    except Exception as e:
        print(e)
