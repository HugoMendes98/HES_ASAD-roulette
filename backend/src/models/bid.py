from datetime import datetime
from . import db

# IDK if this is the standard
from models.round import Round




class Bid(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # it's deprecated, but I don't care
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # max is 9'999'999.99
    wager = db.Column(db.Numeric(10, 2), nullable=False, default=10.0)

    #is the value of the enum
    bet = db.Column(db.Integer, nullable=False)

    # is null when not decided true if won, false if lost
    is_won = db.Column(db.Boolean, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    round_id = db.Column(db.Integer, db.ForeignKey("round.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)

    # let us get a list of bids from user
    user = db.relationship("User", backref="bids")
    # let us get a list of bids from round
    round = db.relationship("Round", backref="bids")
    # let us get a list of bids from game
    round = db.relationship("Game", backref="bids")

    def __repr__(self):
        return "<Bid %r>" % self.id

    @classmethod
    def new(cls, wager, bet, user_id, round_id):
        n = cls(wager=wager, bet=bet, user_id=user_id, round_id=round_id, game_id=Round.get()) # TODO
        db.session.add(n)
        db.session.commit()
        return n

    @classmethod
    def get_bids_from_user_and_round(cls,user_id,round_id):
        n = db.session.query(Bid).filter_by(user_id=user_id, round_id=round_id).all()
        return n

    @classmethod
    def get_bids_from_user_and_round(cls,user_id,round_id):
        n = db.session.query(Bid).filter_by(user_id=user_id, round_id=round_id).all()
        return n
    
    @classmethod
    def get_bids_from_user(cls,user_id):
        n = db.session.query(Bid).filter_by(user_id=user_id).all()
        return n

    @classmethod
    def get_bids_from_round(cls,round_id):
        n = db.session.query(Bid).filter_by(round_id=round_id).all()
        return n

    # It is possible to have multiple winning bids (red + even),(player 1 + player 2)
    @classmethod
    def get_winning_bids_from_round(cls,round_id):
        n = db.session.query(Bid).filter_by(round_id=round_id,is_won=True).all()
        return n

    # if more specifif getter ar needed, just add them
