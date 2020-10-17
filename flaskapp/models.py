from datetime import datetime
from flaskapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(userId):
    return User.query.get(int(userId))

class Q_form(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(60),nullable = False)
    ab = db.Column(db.String(150),nullable = False)
    def __repr__(self):
        return f"Q_form('{self.email}','{self.ab}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable = False)
    password = db.Column(db.String(60), nullable = False)
    picture = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    db.relationship('post', backref='user', lazy=True)
    def __repr__(self):
        return f"User('{self.email}','{self.username}' )"


class post(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String(20),nullable = False)
    title = db.Column(db.String(20), nullable = False)
    description = db.Column(db.String(150))
    author = db.Column(db.String(60))
    postedBy = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
