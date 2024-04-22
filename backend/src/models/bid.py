from datetime import datetime
from . import db

from . import InOutBets, get_factor_from_InOutBets, Slots


class Bid(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # it's deprecated, but I don't care
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # max is 9'999'999.99
    wager = db.Column(db.Numeric(10, 2), nullable=False, default=10.0)

    # is the value of the enum
    inOutbet = db.Column(db.Integer, nullable=False)

    # is null when not decided true if won, false if lost
    is_won = db.Column(db.Boolean, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    round_id = db.Column(db.Integer, db.ForeignKey("round.id"), nullable=False)

    # Maybe dont store this, and always compute it? But it is too pratctical to have Game.bids
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)

    # let us get a list of bids from user
    user = db.relationship("User", backref="bids")
    # let us get a list of bids from round
    round = db.relationship("Round", backref="bids")
    # let us get a list of bids from game
    game = db.relationship("Game", backref="bids")

    def __repr__(self):
        return "<Bid %r>" % self.id

    @classmethod
    def new(cls, wager, inOutbet: InOutBets, user, round):
        n = cls(
            wager=wager,
            inOutbet=inOutbet.value,
            user_id=user.id,
            round_id=round.id,
            game_id=round.game_id,
        )
        db.session.add(n)
        db.session.commit()
        return n

    '''
    @classmethod
    def get_bids_from_user_and_round(cls, user, round):
        n = db.session.query(cls).filter_by(user_id=user.id, round_id=round.id).all()
        return n
    '''

    @classmethod
    def get_bids_from_user_and_round_with_bet(cls, user, round, player_bet : InOutBets):
        n = db.session.query(cls).filter_by(user_id=user.id, round_id=round.id, inOutbet=player_bet.value).first()
        return n


    @classmethod
    def update_wager(cls, bid_id, new_wager) -> bool:
        n : Bid = cls.query.get(bid_id)
        if n:
            n.wager = new_wager
            db.session.commit()
            return True
        raise Exception("Bid not found.")
    
    @classmethod
    def update_is_won(cls, bid_id, winning_slot:Slots) -> bool:
        n : Bid = cls.query.get(bid_id)
        if n:
            n.is_won = n.inOutbet == winning_slot
            db.session.commit()
            return True
        raise Exception("Bid not found.")

    @classmethod
    def delete_bid(cls, bid_id) -> bool:
        n = cls.query.get(bid_id)
        if n:
            db.session.delete(n)
            db.session.commit()
            return True
        raise Exception("Bid not found.")

    # if more specific getter ar needed, just add them

    def payout(self):
        return self.wager * get_factor_from_InOutBets(self.inOutbet)
