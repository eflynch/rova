from flask import render_template, redirect, url_for
from flask.ext.login import LoginManager, current_user
import json

from rova import app, db

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_anonymous:
        return redirect(url_for('login'))

    return render_template('index.jade', bootstrap=json.dumps({
        'current_user': current_user.to_dict()
    }))

@app.route('/login')
def login():
    return render_template('login.jade')
