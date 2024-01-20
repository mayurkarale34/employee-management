
from flask import Flask, render_template, redirect, request, jsonify,session, flash, url_for, make_response, send_file,Response

from sqlalchemy import create_engine, text
from config import DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOSTNAME, DATABASE_NAME
from flask_caching import Cache
from flask_cors import CORS
import datetime
import calendar
import random
import string
from datetime import datetime, timedelta
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO


from cryptography.fernet import Fernet

from config import ENCRYPTION_KEY

from functools import wraps

from apscheduler.schedulers.background import BackgroundScheduler

def init_engine(app):
    app._engine = create_engine('mysql://' + DATABASE_USERNAME + ':' + DATABASE_PASSWORD + '@' + DATABASE_HOSTNAME + '/' + DATABASE_NAME + '?charset=utf8', echo = False, pool_size = 50, max_overflow = 16, pool_recycle = 300)

app = Flask(__name__)
CORS(app, origins="*")
app.secret_key = '123456'
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.debug = True
init_engine(app)


def init_add_attedance():
    # Schedule method call
    scheduler_add_attendance = BackgroundScheduler(daemon = True)
    scheduler_add_attendance.add_job(func = auto_add_attendance, trigger = 'cron', day = '*', hour ='*', minute =37, second =00)
    scheduler_add_attendance.start()