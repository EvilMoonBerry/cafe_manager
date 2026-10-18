import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

load_dotenv()

#client =MongoClient(os.environ["MONGO_URI"], serverSelectionTimeoutMS=3000)
#print("Database:", client.list_database_names())

# Sources used for syntax and understanding different concepts of MongoDB https://www.w3schools.com/python/python_mongodb_getstarted.asp ,https://www.mongodb.com/resources/languages/python

class MongoCafe:
    def __init__ (self, col, req, opt):
        client =MongoClient(os.environ["MONGO_URI"], serverSelectionTimeoutMS=3000)
        self.col = client["cafe"][col]
        self.req = req
        self.opt = opt

# Lists all items from database
    def list_all(self):
        customers = []
        for s in self.col.find().sort("name"):
            s["id"] = str(s.pop("_id"))
            customers.append(s)
        return customers
    
# Fetches one item from database
    def get(self, custo_id):
        if not ObjectId.is_valid(custo_id):
            return None
        customer = self.col.find_one({"_id": ObjectId(custo_id)})
        if customer is None:
            return None
        customer["id"] = str(customer.pop("_id"))
        return customer

# Adds one item to the database
    def add(self, data):
        customer = {i: data[i] for i in self.req}
        for i in self.opt:
            val = data.get(i)
            if val is not None and val != "" and val != []:
                customer[i] = val
        new_cust= self.col.insert_one(customer)
        return str(new_cust.inserted_id)

# Updates existing item in database
    def update(self, custo_id, data):
        addition = {i: data[i] for i in self.req}
        move = {}
        for i in self.opt:
            val = data.get(i)
            if val is None or val == "" or val==[]:
                move[i] = ""
            else:
                addition[i]=data[i]
        change = {"$set":addition}
        if move:
            change["$unset"] = move
        self.col.update_one({"_id": ObjectId(custo_id)}, change)

# Deletes item from database
    def delete(self,custo_id):
        self.col.delete_one({"_id": ObjectId(custo_id)})

cafe_customers = MongoCafe(
    "customers",
    req = ["name", "email", "points"],
    opt=["birthday","favourite_drinks"],
)

