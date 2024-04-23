from datetime import datetime
from . import db

from . import Bid
from . import User
from . import InOutBets, Slots, RoundStates


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    state = db.Column(db.Integer, nullable=False, default=RoundStates.IDLE.value)

    # it's deprecated, but I don't care
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    next_state_timestamp = db.Column(db.DateTime)

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
    def new(cls, round_number, game, next_state_timestamp=None):
        new_round = cls(round_number=round_number, game_id=game.id, next_state_timestamp=next_state_timestamp)
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
        winning_bids_out = []
        for bid in winning_bids:
            winnings = bid.payout()
            winner = User.get_by_id(bid.user_id)
            new_balance = winnings + winner.balance
            User.update_balance(
                user_id=bid.user_id, new_balance=new_balance
            )
            winning_bids_out.append({"username":winner.username, "winnings":winnings, "new_balance": new_balance})
        return winning_bids_out

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

    def update_state(self, new_state: InOutBets, next_state_timestamp=None) -> bool:
        self.state = new_state.value
        self.next_state_timestamp = next_state_timestamp
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

    def to_dict(self):
        state = RoundStates(self.state)
        round_dict = dict(state=state.name)
        if self.next_state_timestamp is not None:
            next_state = (self.next_state_timestamp - datetime.utcnow()).total_seconds()
            next_state = 0 if next_state < 0 else next_state
            round_dict["next_state_seconds"] = next_state
        if state == RoundStates.BIDABLE:
            bets = {bet.inOutbet: {"username": bet.user.username, "value": int(bet.wager)} for bet in self.bids}
            round_dict["bets"] = bets
        elif state == RoundStates.RESULT:
            round_dict["winning_slot"] = self.winning_slot
        elif state == RoundStates.IDLE:
            pass
        elif state == RoundStates.WAITING:
            pass
        return round_dict