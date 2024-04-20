from datetime import datetime
from . import db

class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    state = db.Column(db.Integer, nullable=False)

    # it's deprecated, but I don't care
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # might be useless
    number = db.Column(db.Integer, nullable=False)
    game_id = db.Column(db.Integer, nullable=False)

    # let us get a list of round from game
    game = db.relationship("Game", backref="rounds")

    
    def __repr__(self):
        return '<Round %r>' % self.id