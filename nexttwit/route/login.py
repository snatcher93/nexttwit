# -*- encoding: utf-8 -*-
from flask import render_template, redirect, g, request, session, url_for
from userdao import userDao
from server import app
from user import User

# 여기에 원하는 주소를 입력하세요
@app.route('/')
def login():
    if g.user:
        return redirect(url_for('public_timeline'))
        
    # 여기에 html 페이지 이름을 입력하세요
    return render_template('', error=None)

@app.route('/login', methods=['POST'])
def doLogin():
    error = None

    if request.method == 'POST':
        user = userDao.findByUserId(request.form['userid'])
        if user is None:
            error = u"존재하지 않는 아이디입니다"
        elif request.form['password'] != user.password:
            error = u"비밀번호가 올바르지 않습니다"
        else:
            session['user_id'] = user.userid
            return redirect(url_for('public_timeline'))
        
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        if not request.form.get('userid'):
            error = u"아이디를 입력해주세요"
        elif not request.form.get('email') or '@' not in request.form.get('email'):
            error = u'올바른 이메일 주소를 입려해주세요'
        elif not request.form.get('password'):
            error = u'비밀번호를 입력해주세요'
        elif request.form.get('password') != request.form.get('repassword'):
            error = u'입력하신 두 비밀번호가 동일하지 않습니다'
        elif userDao.findByUserId(request.form.get('userid')):
            error = u'사용자가 이미 존재합니다'
        else:
            user = User(request.form.get('userid'), request.form.get('email'), request.form.get('password'))
            userDao.save(user)
            return redirect(url_for('login'))

    return render_template("signup.html", error=error)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))
