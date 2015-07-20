from flask import Blueprint, jsonify, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user

from passlib.hash import sha256_crypt

from rova import db
from rova.models import User

api = Blueprint('api', __name__)

class APIException(Exception):
    def __init__(self, status, message=None):
        self._status = status
        self._message = message
    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, value):
        self._status = value
    @property
    def message(self):
        if self._message:
            return self._message
        if self._status == 404:
            return 'Not found'
        if self._status == 403:
            return 'Forbidden'
        if self._status == 401:
            return 'Unauthorized'
        if self._status == 400:
            return 'Bad request'
    @message.setter
    def message(self, value):
        self._message = value

@api.errorhandler(APIException)
def handle_api_exception(error):
    resp = jsonify({'message': error.message, 'status': error.status})
    resp.status_code = error.status
    return resp

@api.before_request
def verify_api():
    if 'application/json' not in request.content_type:
        raise APIException(400, 'Requires JSON')

@api.route('/users', methods=['POST'])
def createUser():
    username = request.json.get('username')
    password = request.json.get('password')
    user = db.session.query(User).filter(User.username==username).first()
    if user:
        raise APIException(400, message="Username unavailable")
    if len(password) < 10:
        raise APIException(400, message="Password too short")
    passhash = sha256_crypt.encrypt(password)
    newUser = User(username, passhash)
    db.session.add(newUser)
    db.session.commit()
    return jsonify(newUser.to_dict())

@api.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = db.session.query(User).filter(User.username==username).first()
    if not user:
        raise APIException(403)
    if not sha256_crypt.verify(password, user.passhash):
        raise APIException(403)

    login_user(user)
    return jsonify({'message': 'Success!'})

@api.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Success!'})
