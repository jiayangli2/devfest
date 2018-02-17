from flask import Flask, request, render_template, g, redirect, Response, session, escape, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import populate from helper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ubuntu/devfest/app.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(80), primary_key=True, nullable=False)
    fullname = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)


    def __repr__(self):
        return '<User %r>' % self.username



@app.route('/')
def index():

    # DEBUG: this is debugging code to see what request looks like
  print (request.args)

  names = ["grace hopper", "alan turing", "ada lovelace"]
  context = dict(data = names)

  return render_template("index.html", **context)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        try:
            temp = User.query.filter_by(username=uname).first()
            if temp == None || temp.password != pwd:
                err_msg = "incorrect username or password"
                context = dict(data = err_msg)
                render_template("error.html", **context)
            else:
                populate(session, temp)
                return redirect(url_for('index'))
        except:
            err_msg = "connection to DB failed"
            context = dict(data = err_msg)
            render_template("error.html", **context)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        fname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phoen']
        user_created = Users(username = uname, fullname = fname, password = pwd, phone = phone, email = email)
        try:
            db.session.add(user_created)
            db.session.commit()
        except:
            return "Sign Up Failed!"

        populate(session, user_created)
        return render_template("index.html")
    elif request.method == 'GET':
        return render_template("signup.html")
    return "error: request not supported"

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('fullname', None)
    session.pop('phoen', None)
    session.pop('email', None)
    return redirect(url_for('index'))



