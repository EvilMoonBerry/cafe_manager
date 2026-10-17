import os
from dotenv import load_dotenv
from flask import Flask

# https://flask.palletsprojects.com/en/stable/quickstart/ quickstart for Flask

load_dotenv()
mongo_uri = os.environ["MONGO_URI"]

app = Flask(__name__)

@app.route("/")
def home():
    return "Cafe Manager"

if __name__ == "__main__":
    app.run(debug=True)



