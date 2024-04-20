from flask_sqlalchemy import SQLAlchemy
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False) # for now is unique
    balance = db.Column(db.Numeric(10, 2), nullable=False, default=200.00) # starts with 200$
    password_hash = db.Column(db.String(64), nullable=False, default='placehodlerForSLOWHash')
    
    def __repr__(self):
        return '<User %r>' % self.username