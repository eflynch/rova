from rova import db

class User(db.Base):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    passhash = db.Column(db.String(255))
    role = db.Column(db.Integer)

    def __init__(self, username, passhash):
        self.username = username
        self.passhash = passhash
        self.role = 0

    def __repr__(self):
        return '<User %s>' % self.username

    def to_dict(self):
        return {
            'username': self.username,
            'role': self.role
        }

    # Class methods for flask-login

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
