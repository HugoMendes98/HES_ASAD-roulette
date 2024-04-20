from datetime import datetime
from app import db

class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # it's deprecated, but I don't care
    bid = db.Column(db.Numeric(10, 2), nullable=False)
    result = db.Column(db.Boolean, nullable=True) # is null when not decided
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    user = db.relationship('User', backref='bids') # let us get a list of bids from user
    game = db.relationship('Game', backref='bids') # let us get a list of bids from game
    
    def __repr__(self):
        return '<Bid %r>' % self.id