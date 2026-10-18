import os
import sqlite3
from dotenv import load_dotenv
from datetime import datetime
from pymongo import MongoClient

load_dotenv()

SQLITE_DIR = os.environ.get("SQLITE_DIR", "data")
os.makedirs(SQLITE_DIR, exist_ok=True)

# Creating sample data of items sold in the cofee shop and adding them to SQLite database
def cafeMenu_setup():
    path = os.path.join(SQLITE_DIR, "menu.db")
    conn = sqlite3.connect(path)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL CHECK (price >= 0),
            in_stock INTEGER NOT NULL DEFAULT 1 CHECK (in_stock IN (0,1))
        )
    """)

    count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    if count == 0:
        sample_items = [
            ("Black coffee", "Coffee", 3.30, 1),
            ("Espresso", "Coffee", 3.20, 1),
            ("Brewed tea", "Tea", 2.80, 1),
            ("Croissant", "Pastry", 3.10, 1),
            ("Cinnamon bun", "Pastry", 3.30, 0),
        ]
        conn.executemany(
            "INSERT INTO items (name, category, price, in_stock) VALUES (?, ?, ?, ?)",
            sample_items,
        )
        print("menu.db: inserted", len(sample_items), " sample items")
    else:
        print("menu.db: already has", count, " items, skipped")

    conn.commit()
    conn.close()

# Creating sample data of staff who works in the cofee shop adding them to SQLite database
def cafeStaff_setup():
    path = os.path.join(SQLITE_DIR, "staff.db")
    conn = sqlite3.connect(path)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS staff_persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            hourly_wage REAL NOT NULL CHECK (hourly_wage >= 0),
            starting_date TEXT NOT NULL CHECK (date(starting_date)=starting_date)
        )
    """)

    count = conn.execute("SELECT COUNT(*) FROM staff_persons").fetchone()[0]
    if count == 0:
        sample_staff = [
            ("Niilo", "Barista", 18.50, "2025-03-01"),
            ("Nelli", "Barista", 18.50, "2025-8-25"),
            ("Mikko", "Shift manager", 22.50, "2020-5-7"),
            ("Henna", "Manager", 27.50, "2019-10-11"),
        ]
        conn.executemany(
            "INSERT INTO staff_persons (name, role, hourly_wage, starting_date) VALUES (?, ?, ?, ?)",
            sample_staff,
        )
        print("staff.db: inserted", len(sample_staff), " sample staff")
    else:
        print("staff.db: already has", count, " staff, skipped")

    conn.commit()
    conn.close()

# Creating sample data of customers of the cofee shop adding them to MongoDB
def cafeCustomers_setup():
    client =MongoClient(os.environ["MONGO_URI"], serverSelectionTimeoutMS=3000)
    db = client["cafe"]
    customers = db["customers"]

    customers.create_index("email", unique=True)

    count = customers.count_documents({})
    if count == 0:
        sample_customers= [
        {
            "name": "Ninni",
            "email": "ninni@coffee.com",
            "points": 0,
        },
        {
            "name": "Matti",
            "email": "matti@coffee.com",
            "points": 25,
            "birthday": datetime(1997, 1, 4),
            "favourite_drinks": ["Brewed tea","Black coffee"],
        },
        {
            "name": "Jenny",
            "email": "Jenny@coffee.com",
            "points": 120,
            "favourite_drinks": ["Espresso"],
        },
        ]
        customers.insert_many(sample_customers)
        print("Customers (MongoDB): inserted", len(sample_customers), " sample customers")
    else:
        print("Customers (MongoDB): already has", count, " sample customers")

    client.close()

def main():
    cafeMenu_setup()
    cafeStaff_setup()
    cafeCustomers_setup()

if __name__ == "__main__":
    cafeMenu_setup()
    cafeStaff_setup()
    cafeCustomers_setup()

