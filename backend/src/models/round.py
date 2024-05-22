from datetime import datetime

from .bid import Bid
from .db import db
from .round_info import InOutBets, RoundStates, Slots
from .user import User


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

    is_canceled = db.Column(db.Boolean, nullable=False, default=False)

    # let us get a list of round from game
    game = db.relationship(
        "Game", backref="rounds", order_by="Round.round_number.desc()"
    )

    @classmethod
    def new(cls, round_number, game, next_state_timestamp=None, is_txn=False):
        new_round = cls(
            round_number=round_number,
            game_id=game.id,
            next_state_timestamp=next_state_timestamp,
        )
        db.session.add(new_round)
        if not is_txn:
            db.session.commit()
        return new_round

    def __repr__(self):
        return "<Round %r>" % self.id
    
    def canceled_check(self):
        if self.is_canceled:
            raise Exception("Round canceled!")

    # raises error if another player has taken the InOutBet for this round
    # return the player bid if one exists
    # return none if no ones has taken the bet
    def get_bet_on_inOutBet(self, player_bet: InOutBets, player):
        player_bid = Bid.get_bids_from_round_with_bet(round=self, player_bet=player_bet)
        if player_bid:
            if player_bid.user_id != player.id:
                raise Exception("This slot is already taken by other user.")
        return player_bid

    """
        args = {"username": username}
        if password_hash is not None:
            args["password_hash"] = password_hash
        new_user = cls(**args)
        db.session.add(new_user)
        if not is_txn:
            db.session.commit()
        return new_user
        
    """

    def pay_out(self):
        self.canceled_check()
        winning_bids = self.get_winning_bids()
        # in the current version of the roulette, we can only get 1 winner
        winning_bids_out = []
        for bid in winning_bids:
            winnings = bid.payout()
            winner = User.get_by_id(bid.user_id)
            new_balance = winnings + winner.balance
            winner.update_balance(new_balance=new_balance)
            winning_bids_out.append(
                {
                    "username": winner.username,
                    "winnings": winnings,
                    "new_balance": new_balance,
                }
            )
        return winning_bids_out
    
    def cancel_round(self, is_txn=False,):
        self.is_canceled = True
        # give money back
        for bid in self.bids:
            self.refund_player(is_txn=True, bid=bid)
        if not is_txn:
            db.session.commit()

    
    # only use this when a round has been canceled
    def refund_player(self, bid, is_txn=False):
        user = User.get_by_id(bid.user_id)
        user.update_balance(is_txn=True,new_balance=user.balance + bid.wager)
        bid.update_wager(is_txn=True,new_wager=0)
        if not is_txn:
            db.session.commit()

    def update_winning_slot(self, new_winning_slot: Slots, is_txn=False) -> bool:
        self.canceled_check()
        self.winning_slot = new_winning_slot.value
        if not is_txn:
            db.session.commit()

    def update_bids_after_result(self):
        self.canceled_check()
        for bid in self.bids:
            bid.update_is_won(self.winning_slot)

    def update_state(self, new_state, next_state_timestamp=None, is_txn=False) -> bool:
        self.canceled_check()
        self.state = new_state.value
        self.next_state_timestamp = next_state_timestamp
        if not is_txn:
            db.session.commit()
        return True

    """
    @classmethod
    def update_pot(cls, round_id, new_pot, is_txn=False) -> bool:
        n: Round = cls.query.get(round_id)
        if n:
            n.pot = new_pot
            if not is_txn:
                db.session.commit()
            return True
        raise Exception("Round not found.")
    """

    # in the current version, we can only get 1 (or 0) winning bids
    def get_winning_bids(self):
        n = db.session.query(Bid).filter_by(round_id=self.id, is_won=True).all()
        return n
    
    def get_history(self,slot = 19):
        n = db.session.query(Round).filter_by(game_id = self.game_id).filter(Round.winning_slot.isnot(None)).order_by(Round.round_number.desc()).offset(1).limit(slot).all()
        history = []
        for round in n:
            history.append(round.winning_slot)

        return history

    def to_dict(self):
        state = RoundStates(self.state)
        round_dict = {
            "state": state.name,
            "next_state_timestamp": self.next_state_timestamp,
            "last_win" : self.get_history()
        }

        if state == RoundStates.BIDABLE or state == RoundStates.WAITING:
            bets = [
                {
                    "username": bet.user.username,
                    "inOutbet": bet.inOutbet,
                    "wager": int(bet.wager),
                }
                for bet in self.bids
            ]

            round_dict["bets"] = bets
        elif state == RoundStates.RESULT:
            bets = [
                {
                    "username": bet.user.username,
                    "inOutbet": bet.inOutbet,
                    "wager": int(bet.wager),
                }
                for bet in self.bids
            ]

            round_dict["bets"] = bets

            round_dict["pay_out"] = self.pay_out()
            round_dict["winning_slot"] = self.winning_slot
        elif state == RoundStates.IDLE:
            pass

        return round_dict

    def to_json(self):
        state = self.to_dict()
        # * 1000 for JS timestamp
        ts = (
            int(state["next_state_timestamp"].timestamp() * 1000)
            if state["next_state_timestamp"] is not None
            else None
        )
        return {
            **state,
            "next_state_timestamp": ts,
        }
