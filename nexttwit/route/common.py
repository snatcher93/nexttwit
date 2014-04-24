# -*- encoding: utf-8 -*-
from flask import render_template, redirect, g, request, session, url_for
from userdao import userDao
from server import app


@app.before_request
def before():
    g.user = None
    if 'user_id' in session:
        g.user = userDao.findByUserId(session['user_id'])

