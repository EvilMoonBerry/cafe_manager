import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, redirect, url_for
from db.sqlite_cafe import cafe_menu, cafe_staff
from db.mongo_cafe import cafe_customers

# Sources used for syntax and understanding different concepts of Flask:
# https://flask.palletsprojects.com/en/stable/quickstart/ quickstart for Flask
# https://dev.to/prahladyeri/flask-recipe-restful-crud-using-sqlalchemy-3731
# https://codesignal.com/learn/courses/mastering-flask-http-methods/lessons/combining-methods-into-single-endpoints
# https://medium.com/@ruchikabhat5/working-with-databases-in-flask-a-comprehensive-guide-96cc2795a751


app = Flask(__name__)

DATABASES = {
    "menu": {
        "title": "Menu",
        "technology": "SQLite",
        "store": cafe_menu,
        "fields":[
            {"name": "name", "label": "Name", "type": "text", "required": True},
            {"name": "category", "label": "Category", "type": "select", "required": True, "choices": ["Coffee", "Tea", "Pastry"]},
            {"name": "price", "label": "Price (€)", "type": "number", "required": True},
            {"name": "in_stock", "label": "In stock", "type": "checkbox"},
        ],
    },
    "staff": {
            "title": "Staff",
            "technology": "SQLite",
            "store": cafe_staff,
            "fields":[
                {"name": "name", "label": "Name", "type": "text", "required": True},
                {"name": "role", "label": "Role", "type": "select", "required": True, "choices": ["Manager", "Shift manager", "Barista"]},
                {"name": "hourly_wage", "label":"Hourly wage", "type": "number", "required": True},
                {"name": "starting_date", "label": "Starting date", "type":"date","required": True},
            ],
    },
    "customers": {
            "title": "Customers",
            "technology": "MongoDB",
            "store": cafe_customers,
            "fields":[
                {"name": "name", "label": "Name", "type": "text", "required": True},
                {"name": "email", "label": "Email", "type": "email", "required": True},
                {"name": "points", "label":"Points", "type": "number", "required": True},
                {"name": "birthday", "label": "Birthday", "type":"date","in_table": False},
                {"name": "favourite_drinks", "label": "Favourite drinks", "type":"list","in_table": False},
            ],
    },
}


def get_database(name):
    db = DATABASES.get(name)
    return db

@app.context_processor
def dbinjector():
    return {"databases": DATABASES}

@app.route("/")
def home():
    return redirect(url_for("display_table", name = "menu"))

@app.route("/db/<name>")
def display_table(name):
    db = get_database(name)
    rows = db["store"].list_all()
    columns = [f for f in db["fields"] if f.get("in_table", True)]
    return render_template("table.html", name = name, db = db, rows = rows, columns = columns)

if __name__ == "__main__":
    app.run(debug=True)



