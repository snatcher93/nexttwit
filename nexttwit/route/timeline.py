# -*- encoding: utf-8 -*-
from flask import render_template, redirect, g, request, session, url_for, abort
from messagedao import messageDao
from followerdao import followerDao
from userdao import userDao
from server import app

@app.route('/')
def my_timeline():
    if not g.user:
        return redirect(url_for('public_timeline'))
    
    followings = followerDao.findFollowings(g.user.id);
    messages = messageDao.findByAuthors(followings)
    return render_template('timeline.html', messages=messages)

@app.route('/public')
def public_timeline():
    messages = messageDao.findAll()
    return render_template("timeline.html", messages=messages)

@app.route('/<userid>')
def user_timeline(userid):
    if not g.user:
        return redirect(url_for('public_timeline'))
    
    profile_user = userDao.findByUserId(userid)
    if profile_user is None:
        abort(404)
    messages = messageDao.findByAuthor(profile_user)    
    follower = followerDao.find(g.user.id, profile_user.id)    
    return render_template("timeline.html", messages=messages, profile_user=profile_user, followed=follower is not None)
    