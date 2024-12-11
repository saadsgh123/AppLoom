#!/usr/bin/python3
from flask import Flask
from models.engine.db_storage import DBStorage
app = Flask(__name__)
storage = DBStorage()


@app.route('/')
def landing_page():
    return f"{storage.find_all()["username"]}"
