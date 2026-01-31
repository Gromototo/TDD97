from flask import Flask
from flask_sock import Sock
import sqlite3

app = Flask(__name__)
sock = Sock(app)

import TWIDDER.views

@app.cli.command('init-db')
def init_db():
    with sqlite3.connect('database.db') as connect:
        with app.open_resource('schema.sql', mode='r') as f:
            connect.executescript(f.read())
    print('Initialized the database.')
