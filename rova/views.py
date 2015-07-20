from flask import render_template
from flask.ext.login import LoginManager, current_user

from rova import app, db

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.jade', bootstrap="dude")
