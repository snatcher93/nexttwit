# -*- encoding: utf-8 -*-
from flask import render_template, redirect, g, request, session, url_for
from messagedao import messageDao
from message import Message
from server import app

@app.route('/twit', methods=['POST'])
def twit():
    message = Message(g.user.id, request.form['message'])
    messageDao.save(message)
    return render_template(url_for('public_timeline'))

@app.route('/retwit', methods=['POST'])
def retwit():
    if not g.user:
        abort(401)

    message = messageDao.findOne(request.form['msgId'])
    if not message:
        abort(400)
        
    retwit = Message(g.user.id, message.message, message)
    messageDao.save(retwit)    
    return redirect(url_for('public_timeline'))
