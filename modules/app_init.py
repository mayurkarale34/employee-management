
from flask import Flask, render_template, redirect, request, jsonify,session, flash, url_for, make_response
from sqlalchemy import create_engine, text
from config import DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOSTNAME, DATABASE_NAME
from flask_caching import Cache
import datetime
import random
import string
from datetime import datetime

from cryptography.fernet import Fernet

from config import ENCRYPTION_KEY

def init_engine(app):
    app._engine = create_engine('mysql://' + DATABASE_USERNAME + ':' + DATABASE_PASSWORD + '@' + DATABASE_HOSTNAME + '/' + DATABASE_NAME + '?charset=utf8', echo = False, pool_size = 50, max_overflow = 16, pool_recycle = 300)

app = Flask(__name__)
app.secret_key = '123456'
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.debug = True
init_engine(app)