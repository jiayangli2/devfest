from flask import Flask, request, render_template, g, redirect, Response, session, escape, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import hashlib, uuid
from helper import populate
import urllib
from markupsafe import Markup
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./app.db'#/home/prokingsley/devfest/app.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
salt = uuid.uuid4().hex


class User(db.Model):
    username = db.Column(db.String(80), primary_key=True, nullable=False)
    fullname = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)


    def __repr__(self):
        return '<User %r>' % self.username

class Event(db.Model):
    id = db.Column(db.String(80), primary_key=True, nullable=False)
    host = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(300), nullable=False)
    time = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)


class Attend(db.Model):
    id = db.Column(db.String(80), db.ForeignKey('event.id'), primary_key=True)
    username = db.Column(db.String(80), primary_key=True, nullable=False)


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
    pwd = hashlib.sha512((request.form['password'] + salt).encode('ascii')).hexdigest()
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
        pwd = hashlib.sha512((request.form['password'] + salt).encode('ascii')).hexdigest()
        fname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        user_created = User(username = uname, fullname = fname, password = pwd, phone = phone, email = email)
        try:
            db.session.add(user_created)
            db.session.commit()
            print ("db")
        except:
            err_msg = "Signing up failed!"
            context = dict(data = err_msg)
            return render_template("index.html", **context)
        populate(session, user_created)
        print ("2")
        return redirect(url_for('index'))
    err_msg = "HTTP Request not supported!"
    context = dict(data = err_msg)
    return render_template("index.html", **context)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('fullname', None)
    session.pop('phone', None)
    session.pop('email', None)
    return redirect(url_for('index'))


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run()
