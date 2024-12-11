#!/usr/bin/python3
from flask import Flask
from models.engine.db_storage import client
app = Flask(__name__)


@app.route('/')
def landing_page():
    db = client["saad"]
    collection = db["users"]
    return f"{collection.find()}"
