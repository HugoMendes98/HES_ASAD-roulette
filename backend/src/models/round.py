from datetime import datetime
from . import db

from . import Bid
from . import User
from . import InOutBets, Slots, RoundStates


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    state = db.Column(db.Integer, nullable=False, default=RoundStates.IDLE.value[1])

    # it's deprecated, but I don't care
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    round_number = db.Column(db.Integer, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)

    # pot = db.Column(db.Integer, nullable=False, default=0)
    winning_slot = db.Column(db.Integer, nullable=True)

    # let us get a list of round from game
    game = db.relationship(
        "Game", backref="rounds", order_by="Round.round_number.desc()"
    )

    def __repr__(self):
        return "<Round %r>" % self.id

    @classmethod
    def new(cls, round_number, game):
        args = {"round_number": round_number, "game_id": game.id}
        new_round = cls(**args)
        db.session.add(new_round)
        db.session.commit()
        return new_round

    """
        args = {"username": username}
        if password_hash is not None:
            args["password_hash"] = password_hash
        new_user = cls(**args)
        db.session.add(new_user)
        db.session.commit()
        return new_user
        
    """

    def pay_out(self):
        winning_bids = self.get_winning_bids()
        # in the current version of the roulette, we can only get 1 winner
        for bid in winning_bids:
            winnings = bid.payout()
            winner = User.get_by_id(bid.user_id)
            new_balance = winnings + winner.balance
            User.update_balance(
                user_id=bid.user_id, new_balance=new_balance
            )

    @classmethod
    def update_winning_slot(cls, round_id, new_winning_slot: Slots) -> bool:
        n: Round = cls.query.get(round_id)
        if n:
            n.winning_slot = new_winning_slot.value
            db.session.commit()
            return True
        raise Exception("Round not found.")

    def update_bids_after_result(self):
        for bid in self.bids:
            Bid.update_is_won(bid.id, self.winning_slot)

    def update_state(self, new_state: InOutBets) -> bool:
        self.state = new_state.value[1]
        db.session.commit()
        return True

    """
    @classmethod
    def update_pot(cls, round_id, new_pot) -> bool:
        n: Round = cls.query.get(round_id)
        if n:
            n.pot = new_pot
            db.session.commit()
            return True
        raise Exception("Round not found.")
    """

    # in the current version, we can only get 1 (or 0) winning bids
    def get_winning_bids(self):
        n = db.session.query(Bid).filter_by(round_id=self.id, is_won=True).all()
        return n