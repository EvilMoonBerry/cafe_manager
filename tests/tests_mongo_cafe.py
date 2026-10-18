from dotenv import load_dotenv
from datetime import datetime
from db.mongo_cafe import cafe_customers

# Tests for the functionalities for manipulating

print(cafe_customers.list_all())

customers = cafe_customers.list_all()

print(cafe_customers.get(customers[0]["id"]))

new_customer = cafe_customers.add({
    "name": "johan",
    "email": "johan@coffee.com",
    "points": 5,
    "birthday": datetime(2006, 7, 10),
    "favourite_drinks": ["Black coffee"],
})

print("New customer added to mongoDB: ", cafe_customers.get(new_customer))

cafe_customers.update(new_customer, {
    "name": "johan",
    "email": "johan@coffee.com",
    "points": 5,
    "favourite_drinks": ["Black coffee"],
})

print("Updated customer in MongoDB: ", cafe_customers.get(new_customer))

cafe_customers.delete(new_customer)
print("Deleted person from Mongo.db: ", cafe_customers.get(new_customer))
