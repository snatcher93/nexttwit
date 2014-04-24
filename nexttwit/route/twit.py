# -*- encoding: utf-8 -*-
from flask import render_template, redirect, g, request, session, url_for
from messagedao import messageDao
from dbgateway import database
from message import Message
from server import app

# 여기에 원하는 주소를 입력하세요
@app.route('/', methods=['POST'])
def twit():
    message = Message(g.user, '여기에 메시지 정보를 넣으세요')
    
    # 여기에 메시지를 기록하기 위한 코드를 넣으세요
    
    # 여기에 html 페이지 이름을 입력하세요
    return render_template('', messages = messageBox, timeline="public")

@app.route('/retwit', methods=['POST'])
def retwit():
    if not g.user:
        abort(401)

    message = messageDao.findOne(request.form['msgId'])
    if not message:
        abort(400)
        
    retwit = Message(g.user, message.message, message)
    messageDao.save(retwit)    
    return redirect(url_for('public_timeline'))
