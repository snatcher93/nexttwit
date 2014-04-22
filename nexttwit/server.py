# -*- encoding: utf-8 -*-

from flask import Flask, render_template, g, request, redirect, url_for, session, abort
import os
from database import initializeDB
from datetime import datetime
from hashlib import md5

def format_datetime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')

def gravatar_url(email, size=80):
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

def createServer():    
    app = Flask(__name__)
    app.config.from_pyfile('minitwit.cfg', silent=True)
    
    app.jinja_env.filters['datetimeformat'] = format_datetime
    app.jinja_env.filters['gravatar'] = gravatar_url
    
    db_filepath = os.path.join(app.root_path, app.config['DB_FILE_PATH'])
    db_url = app.config['DB_URL'] + db_filepath
    initializeDB(db_url, eval(app.config['DB_LOG_FLAG']))
    
    return app

app = createServer()