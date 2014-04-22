# -*- encoding: utf-8 -*-
from flask import Flask, render_template, g, request, redirect, url_for, session, abort
import os
from database import DBManager
from user import User
from follower import Follower
from message import Message
from datetime import datetime
from hashlib import md5

# jinja2 filter
def format_datetime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')

def gravatar_url(email, size=80):
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), 
         size)

# flask application setup
app = Flask(__name__)

# properties
app.config.from_pyfile('resource/minitwit.cfg', silent=True)

# filter
app.jinja_env.filters['datetimeformat'] = format_datetime
app.jinja_env.filters['gravatar'] = gravatar_url

# database 
db_filepath = os.path.join(app.root_path, app.config['DB_FILE_PATH'])
db_url = app.config['DB_URL'] + db_filepath
DBManager.init(db_url, eval(app.config['DB_LOG_FLAG']))    
DBManager.init_db()

from userdao import userDao
from messagedao import messageDao
from followerdao import followerDao

@app.before_request
def before():
    g.user = None
    if 'user_id' in session:
        g.user = userDao.findByName(session['user_id'])

@app.route('/message/add', methods=['POST'])
def addMessage():
    message = Message(g.user.id, request.form['message'])
    messageDao.save(message)
    return redirect(url_for('public_timeline'))

@app.route('/retwit/', methods=['POST'])
def retwit():
    if not g.user:
        abort(401)

    message = messageDao.findOne(request.form['msgId'])
    if not message:
        abort(400)
        
    retwit = Message(g.user.id, message.message, message)
    messageDao.save(retwit)    
    return redirect(url_for('public_timeline'))

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

@app.route('/<username>')
def user_timeline(username):
    if not g.user:
        return redirect(url_for('public_timeline'))
    
    profile_user = userDao.findByName(username)
    if profile_user is None:
        abort(404)
    messages = messageDao.findByAuthor(profile_user)    
    follower = followerDao.find(g.user.id, profile_user.id)    
    return render_template("timeline.html", messages=messages, profile_user=profile_user, followed=follower is not None)

@app.route('/home')
def landing():
    return render_template("landing.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        if not request.form.get('username'):
            error = u"아이디를 입력해주세요"
        elif not request.form.get('email') or '@' not in request.form.get('email'):
            error = u'올바른 이메일 주소를 입려해주세요'
        elif not request.form.get('password'):
            error = u'비밀번호를 입력해주세요'
        elif request.form.get('password') != request.form.get('repassword'):
            error = u'입력하신 두 비밀번호가 동일하지 않습니다'
        elif userDao.findByName(request.form.get('username')):
            error = u'사용자가 이미 존재합니다'
        else:
            user = User(request.form.get('username'), request.form.get('email'), request.form.get('password'))
            userDao.save(user)
            return redirect(url_for('signin'))

    return render_template("signup.html", error=error)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if g.user:
        return redirect(url_for('public_timeline'))

    error = None
    if request.method == 'POST':
        user = userDao.findByName(request.form.get('username'))
        if user is None:
            error = u"존재하지 않는 아이디입니다"
        elif request.form.get('password') != user.password:
            error = u"비밀번호가 올바르지 않습니다"
        else:
            session['user_id'] = user.username
            return redirect(url_for('public_timeline'))
    
    return render_template("signin.html", error=error)

@app.route('/signout')
def signout():
    session.pop('user_id', None)
    return redirect(url_for('landing'))

@app.route('/<username>/follow', methods=['POST'])
def follow_user(username):
    if not g.user:
        abort(401)
    
    whom = userDao.findByName(username)
    follower = Follower(g.user.id, whom.id)
    followerDao.save(follower)
    return redirect(url_for('user_timeline', username=username))

@app.route('/<username>/unfollow', methods=['POST'])
def unfollow_user(username):
    if not g.user:
        abort(401)
    
    whom = userDao.findByName(username)
    follower = followerDao.find(g.user.id, whom.id)
    followerDao.delete(follower)
    return redirect(url_for('user_timeline', username=username))
    
if __name__ == "__main__":
    #init_db()
    app.run(debug=True)