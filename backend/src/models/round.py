from datetime import datetime
from . import db

from .bid import Bid
from .__init__ import InOutBets


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    state = db.Column(db.Integer, nullable=False)

    # it's deprecated, but I don't care
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    round_number = db.Column(db.Integer, nullable=False)
    game_id = db.Column(db.Integer,  db.ForeignKey("game.id"), nullable=False)

    pot = db.Column(db.Integer, nullable=False, default=0)

    # let us get a list of round from game
    game = db.relationship("Game", backref="rounds")

    
    def __repr__(self):
        return '<Round %r>' % self.id
    
    @classmethod
    def new(cls, round_number, game):
        n = cls(round_number=round_number, game_id=game.id)
        db.session.add(n)
        db.session.commit()
        return n

    evaluate # distiribue les prix
    # when the round
    def pay_out(self):
        winning_bids = self.get_winning_bids()
        for bid in winning_bids:
            winnings = bid.payout()
            

    @classmethod
    def update_state(cls, round_id, new_state: InOutBets) -> bool:
        n: Round = cls.query.get(round_id)
        if n:
            n.state = new_state
            db.session.commit()
            return True
        raise Exception("Round not found.")

    @classmethod
    def update_pot(cls, round_id, new_pot) -> bool:
        n: Round = cls.query.get(round_id)
        if n:
            n.pot = new_pot
            db.session.commit()
            return True
        raise Exception("Round not found.")

    # It is possible to have multiple winning bids (red + even),(player 1 + player 2)
    # but never on the same InOutBet
    def get_winning_bids(self):
        n = self.bids.filter_by(is_won=True).all()
        #n = db.session.query(Bid).filter_by(round_id=self.id, is_won=True).all()
        return n






