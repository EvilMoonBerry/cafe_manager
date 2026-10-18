import os
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, abort
from pymongo.errors import DuplicateKeyError
from db.sqlite_cafe import cafe_menu, cafe_staff
from db.mongo_cafe import cafe_customers


# Sources used for syntax and understanding different concepts of Flask:
# https://flask.palletsprojects.com/en/stable/quickstart/ quickstart for Flask
# https://dev.to/prahladyeri/flask-recipe-restful-crud-using-sqlalchemy-3731
# https://codesignal.com/learn/courses/mastering-flask-http-methods/lessons/combining-methods-into-single-endpoints
# https://medium.com/@ruchikabhat5/working-with-databases-in-flask-a-comprehensive-guide-96cc2795a751
# https://jinja.palletsprojects.com/en/stable/templates/


app = Flask(__name__)


DATABASES = {
    "menu": {
        "title": "Menu",
        "technology": "SQLite",
        "cafe": cafe_menu,
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
            "cafe": cafe_staff,
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
            "cafe": cafe_customers,
            "fields":[
                {"name": "name", "label": "Name", "type": "text", "required": True},
                {"name": "email", "label": "Email", "type": "email", "required": True},
                {"name": "points", "label":"Points", "type": "integer", "required": True},
                {"name": "birthday", "label": "Birthday", "type":"date","in_table": False},
                {"name": "favourite_drinks", "label": "Favourite drinks", "type":"list","in_table": False},
            ],
    },
}


def get_database(name):
    db = DATABASES.get(name)
    if db is None:
        abort(404, description=f"There is no database called '{name}'")
    return db

# Help converting data from form to text and python values

# Turn text into right types before saving
def form_to_data(db, form):
    data = {}
    for field in db["fields"]:
        key = field["name"]
        type = field["type"]
        all = form.get(key,"").strip()

        if type == "checkbox":
            data[key] = 1 if key in form else 0
        elif type == "number":
            data[key] = float(all) if all else None
        elif type == "integer":
            data[key] = int(all) if all else None
        elif type == "list":
            data[key] = [part.strip() for part in all.split(",") if part.strip()]
        elif type == "date" and db["technology"] == "MongoDB":
            data[key] = datetime.strptime(all, "%Y-%m-%d") if all else None
        else:
            data[key] = all
    return data

#Turn values into text for from
def row_to_form(db, row):
    values = {}
    for field in db["fields"]:
        key = field["name"]
        value = row.get(key)
        if value is None:
            values[key] = ""
        elif field["type"] == "list":
            values[key] = ", ".join(value)
        elif isinstance(value, datetime):
            values[key] = value.strftime("%Y-%m-%d")
        else:
            values[key] = value
    return values


@app.context_processor
def dbinjector():
    return {"databases": DATABASES}

@app.route("/")
def home():
    return redirect(url_for("display_table", name = "menu"))

@app.route("/db/<name>")
def display_table(name):
    db = get_database(name)
    rows = db["cafe"].list_all()
    columns = [f for f in db["fields"] if f.get("in_table", True)] #skip fiels that are not filled in
    return render_template("table.html", name = name, db = db, rows = rows, columns = columns)

# Add new row to database
@app.route("/db/<name>/add", methods=["GET", "POST"])
def add_row(name):
    db = get_database(name)
    if request.method == "POST":
        data = form_to_data(db, request.form)
        try:
            db["cafe"].add(data)
        except DuplicateKeyError:
            return render_template("form.html", name = name, db = db, values = request.form, record_id = None, error="Another customer already uses this email",), 400
        return redirect(url_for("display_table", name=name))
    return render_template("form.html", name = name, db = db, values = {}, record_id = None)

# Edit existing database
@app.route("/db/<name>/edit/<record_id>", methods=["GET", "POST"])
def edit_row(name, record_id):
    db = get_database(name)
    row = db["cafe"].get(record_id)
    if row is None:
        abort(404, description="may have been deleted")
    if request.method == "POST":
        data = form_to_data(db, request.form)
        try:
            db["cafe"].update(record_id, data)
        except DuplicateKeyError:
            return render_template("form.html", name = name, db = db, values = request.form, record_id = record_id, error="Another customer already uses this email",), 400
        return redirect(url_for("display_table", name=name))
    values = row_to_form(db, row)
    return render_template("form.html", name = name, db = db, values = values, record_id = record_id)

# Delete row from database
@app.route("/db/<name>/delete/<record_id>", methods=["POST"])
def delete_row(name, record_id):
    db = get_database(name)
    db["cafe"].delete(record_id)
    return redirect(url_for("display_table", name = name))




if __name__ == "__main__":
    app.run(debug=True)
