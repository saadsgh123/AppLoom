#!/usr/bin/python3
from flask import Flask
from models.engine.db_storage import DBStorage
app = Flask(__name__)
storage = DBStorage()


@app.route('/')
def landing_page():
    print(f"{type(storage.find_all())}")
    return "<H1> hELLO APPLOOM</H1>"
