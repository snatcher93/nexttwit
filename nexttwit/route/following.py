# -*- encoding: utf-8 -*-
from flask import render_template, redirect, g, request, session, url_for
from follower import Follower
from userdao import userDao
from followerdao import followerDao
from server import app

@app.route('/<userid>/follow', methods=['POST'])
def follow_user(userid):
    if not g.user:
        abort(401)
    
    whom = userDao.findByName(userid)
    follower = Follower(g.user.id, whom.id)
    followerDao.save(follower)
    return redirect(url_for('user_timeline', userid=userid))

@app.route('/<userid>/unfollow', methods=['POST'])
def unfollow_user(userid):
    if not g.user:
        abort(401)
    
    whom = userDao.findByName(userid)
    follower = followerDao.find(g.user.id, whom.id)
    followerDao.delete(follower)
    return redirect(url_for('user_timeline', userid=userid))
