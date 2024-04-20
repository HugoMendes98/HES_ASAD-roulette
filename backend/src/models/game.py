from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, nullable=False, default=0)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # it's deprecated, but I don't care
    bid = db.Column(db.Numeric(10, 2), nullable=False)
    result = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='games') # let us get a list of game from user
    
    def __repr__(self):
        return '<Game %r>' % self.id