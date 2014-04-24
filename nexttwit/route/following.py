# -*- encoding: utf-8 -*-
from flask import render_template, redirect, g, request, session, url_for
from follower import Follower
from userdao import userDao
from followerdao import followerDao
from server import app
from dbgateway import database 

# 여기에 원하는 주소를 입력하세요
@app.route('/', methods=['POST'])
def follow_user():
    if not g.user:
        abort(401)
    
    # userid를 이용해 사용자 정보를 읽어 오도록 수정하세요
    whom = database.findUser('#여기를 수정하시면 됩니다')
    follower = Follower(g.user, whom)
    
    # database.saveFollower()를 이용해 follower를 저장하세요
    
    
    return redirect(url_for('user_timeline', userid=request.form['userid']))

@app.route('/unfollow', methods=['POST'])
def unfollow_user():
    if not g.user:
        abort(401)
        
    whom = database.findUser(request.form['userid'])
    follower = followerDao.find(g.user.id, whom.id)
    followerDao.delete(follower)
    return redirect(url_for('user_timeline', userid=request.form['userid']))
