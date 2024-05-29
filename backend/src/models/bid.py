from datetime import datetime

from .db import db
from .round_info import InOutBets, get_factor_from_InOutBets
#from .user import User

class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # it's deprecated, but I don't care
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # max is 9'999'999.99
    wager = db.Column(db.Integer, nullable=False, default=10.0)

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

    @staticmethod
    def is_wager_positive(wager) -> bool:
        if wager == 0:
            raise Exception("Wager is 0")
        return wager >= 0

    @classmethod
    def new(cls, wager, inOutbet: InOutBets, user, round, is_txn=False):
        n = cls(
            wager=wager,
            inOutbet=inOutbet.value,
            user_id=user.id,
            round_id=round.id,
            game_id=round.game_id,
        )
        db.session.add(n)
        if not is_txn:
            db.session.commit()
        return n

    @classmethod
    def get_bids_from_round_with_bet(cls, round, player_bet: InOutBets):
        n = (
            db.session.query(cls)
            .filter_by(round_id=round.id, inOutbet=player_bet.value)
            .one_or_none()
        )
        return n

    def delete_bid(self, is_txn=False):
        db.session.delete(self)
        if not is_txn:
            db.session.commit()

    def __repr__(self):
        return "<Bid %r>" % self.id

    """
    @classmethod
    def get_bids_from_user_and_round(cls, user, round):
        n = db.session.query(cls).filter_by(user_id=user.id, round_id=round.id).all()
        return n
    """

    """ Deprecated, useful only if multiple player can bet on same InOutBets
    @classmethod
    def get_bids_from_user_and_round_with_bet(cls, user, round, player_bet : InOutBets):
        n = db.session.query(cls).filter_by(user_id=user.id, round_id=round.id, inOutbet=player_bet.value).first()
        return n
    """

    def update_wager(self, new_wager, is_txn=False):
        self.wager = new_wager
        if not is_txn:
            db.session.commit()

    def update_is_won(self, winning_slot, is_txn=False):
        self.is_won = self.inOutbet == winning_slot
        if not is_txn:
            db.session.commit()

    def payout(self):
        return self.wager * get_factor_from_InOutBets(self.inOutbet)
