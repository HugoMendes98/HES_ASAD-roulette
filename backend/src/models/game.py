from datetime import datetime
from app import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    round = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return '<Game %r>' % self.id