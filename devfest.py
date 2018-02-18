from flask import Flask, request, render_template, g, redirect, Response, session, escape, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import hashlib
from helper import populate
import urllib
from markupsafe import Markup
import sys
import time
from nlp import parser

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./app.db'#/home/prokingsley/devfest/app.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
salt = 'cdea050d7d604afea194572ef22d5297'


class User(db.Model):
    username = db.Column(db.String(80), primary_key=True, nullable=False)
    fullname = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Event(db.Model):
    eid = db.Column(db.String(80), primary_key=True, nullable=False)
    host = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(300), nullable=False)
    time = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return '<Event %r>' % self.message


class Attend(db.Model):
    eid = db.Column(db.String(80), db.ForeignKey('event.eid'), primary_key=True)
    username = db.Column(db.String(80), primary_key=True, nullable=False)
    def __repr__(self):
        return '<eid %r>' % self.eid



@app.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.quote_plus(s)
    return Markup(s)


@app.route('/')
def index():

    # DEBUG: this is debugging code to see what request looks like
    print (request.args)

    #names = ["grace hopper", "alan turing", "ada lovelace"]
    names = {"grace hopper":[123,"hi"], "alan turing":[456, "yeah"]}
    context = dict(data = names)

    return render_template("index.html", **context)


@app.route('/login', methods=['POST'])
def login():
    uname = request.form['username']
    pwd = hashlib.sha512(request.form['password'] + salt).hexdigest()
    try:
        temp = User.query.filter_by(username=uname).first()
        if temp == None or temp.password != pwd:
            err_msg = "incorrect username or password"
            context = dict(data = err_msg)
            print ("no such user")
            return render_template("index.html", **context)
        else:
            populate(session, temp)
            return redirect(url_for('index'))
    except:
        err_msg = "connection to DB failed"
        context = dict(data = err_msg)
        return render_template("index.html", **context)


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        print ("hello world!")
        uname = request.form['username']
        pwd = hashlib.sha512(request.form['password'] + salt).hexdigest()
        fname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        app.logger.info('%s logged in successfully', uname)
        user_created = User(username = uname, fullname = fname, password = pwd, phone = phone, email = email)
        try:
            db.session.add(user_created)
            db.session.commit()
        except:
            err_msg = "Signing up failed!"
            context = dict(data = err_msg)
            return render_template("index.html", **context)
        populate(session, user_created)
        return redirect(url_for('index'))
    err_msg = "HTTP Request not supported!"
    context = dict(data = err_msg)
    return render_template("index.html", **context)

@app.route('/event', methods=['POST'])
def createEvent():
    eid = "%.3f" % (time.time())
    host = request.form['host']
    message = request.form['message']
    event_time = request.form['time']
    location = request.form['location']
    
    (tokens, actions_list) = parser(message)
    if len(actions_list) == 0:
        actions_list.append(message)

    event_created = Event(eid = eid, host = host, message = actions_list[0] , time = event_time, location = location)

    try:
        db.session.add(event_created)
        db.session.commit()
        print ("sdiuhqwiudhiwqdhiuahd")
    except:
        err_msg = "Create Event Failed!"
        context = dict(data = err_msg)
        return render_template("index.html", **context)
    print ("Create Event Succeeded!")
    return redirect(url_for('events'))

@app.route('/attend/<eid>/<username>', methods=['POST'])
def attendEvent():
    attend_event = Attend(eid=eid, username=username)
    try:
        db.session.add(attend_event)
        db.session.commit()
    except:
        err_msg = "Join Event Failed!"
        context = dict(data = err_msg)
        return render_template("index.html", **context)
    print ("Attend Event Succeeded!")
    return redirect(url_for('events'))

@app.route('/logout')
def logout():
    for key in session.keys():
        session.pop(key)
    return redirect(url_for('index'))


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0',debug=True)
