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
        self.db.items.insert_one(
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
        )
    
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
        self.item = item
        self.status = status
        self.buyer = buyer
        self.quantity = 1


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

    def GetGender(self):
        return self.gender
    
    def GetDOB(self):
        return self.DOB
    
    def GetimId(self):
        return self.imId
    
    def GetbioId(self):
        return self.bioID

    def GetuserName(self):
        return self.username


class Customer(Person):
    def __init__(self, name, email, telephone, address, db, city, username, password = None):
        self.super.__init__(name, email, telephone, address, db)
        self.city = city
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
    def __init__(self, name, email, telephone, address, db, username, password = None):
        self.super.__init__(name, email, telephone, address, db, username, password)
        self.buyerId = self.iD
        self.history = []
        self.shoppingCart = []
    
    def UpdateDb(self):
        db.users.update_one({"username":self.username},{"$set":{"history":self.history, "shoppingCart":self.shoppingCart}})
    
    def AddToCart(self, item):
        self.shoppingCart.append(item)
        self.UpdateDb()

    def BuyItem(self, item):
        # Sharing contact details
        mail_sender = smtplib.SMTP('smtp.gmail.com', 587)
        mail_sender.starttls()
        mail_sender.login("ospgrp37@gmail.com", "BestTrio123")
        message = "Hi {},\nYou have requested to buy {} through our portal and in order to proceed further you are supposed to contact the seller of the item. The contact details of the seller are:-\n\t\t\tName - {}\n\t\t\tEmail Id - {}\n\t\t\tMobile number - {}\nRegards\nTeam 37".format(self.name, item.name, item.seller.name, item.seller.email, item.seller.telephone)
        mail_sender.sendmail("ospgroup37@gmail.com", self.email, message)
        message = "Hi {},\n{} has requested to buy {} through our portal and order to proceed further you are supposed to contact the buyer. The contact details of the buyer are:-\n\t\t\tName - {}\n\t\t\tEmail Id - {}\n\t\t\tMobile number - {}\nRegards\nTeam 37".format(item.seller.name, item.name, self.name, self.email, self.telephone)
        mail_sender.sendmail("ospgroup37@gmail.com", item.seller.email, message)
        mail_sender.quit()
        # Updating other things
        shoppingCart.remove(item)
        order = Order(item, buyer, False)
        history.append(order)
        self.UpdateDb()
    
    def InitiateNegotiation(self):
        pass

    def AddToDB(self):
        self.db.users.insert_one({
            "name":self.name, 
            "email":self.email, 
            "telephone":self.telephone, 
            "address":self.address, 
            "city":self.city,
            "Id":self.iD
        })
        self.db.buyers.insert_one({
            "username":self.username,
            "shoppingCart":self.shoppingCart,
            "history":self.history
        })

class Seller(Customer):
    pass
    