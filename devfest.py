from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/index', methods=['GET'])
def signup():
    return render_template('index.html')


@app.route('/signup', methods=['POST'])
def create_account():
    return request.form['username'] + request.form['password']


if __name__ == '__main__':
    app.run()
