#!/usr/bin/python3
from flask import Flask
from models.engine.db_storage import client
app = Flask(__name__)


@app.route('/')
def landing_page():

    return client.list_database_names()
