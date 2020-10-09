from datetime import datetime
from flaskapp import db

class Q_form(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(60),nullable = False)
    ab = db.Column(db.String(150),nullable = False)
    def __repr__(self):
        return f"Q_form('{self.email}','{self.ab}')"