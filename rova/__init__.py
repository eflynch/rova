from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.login import LoginManager

app = Flask(__name__)

app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.config.from_object('config')

db = SQLAlchemy(app)
db.Base = declarative_base()

from rova import views, models, api

app.register_blueprint(api.api, url_prefix='/api')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return db.session.query(models.User).filter(
                models.User.username == userid
           ).first()

@login_manager.unauthorized_handler
def unauthorized():
    if 'application/json' in request.content_type:
        resp = jsonify({'message': 'Unauthorized', 'status': 401})
        resp.status_code = 401
        return resp
    return redirect(url_for('login_view'))
