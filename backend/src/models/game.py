from .db import db
from .round import Round
from .round_info import RoundStates


# technically represent a "table"
# maybe ad a "closed" state
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return "<Game %r>" % self.id

    @classmethod
    def get(cls, game_id):
        return db.session.query(cls).filter_by(id=game_id).one_or_none()

    @classmethod
    def new(cls, id_=None, is_txn=False):
        new_game = cls(id=id_)
        db.session.add(new_game)
        if not is_txn:
            db.session.commit()
        return new_game

    def get_last_round(self) -> Round:
        return (
            db.session.query(Round)
            .filter_by(game=self)
            .order_by(Round.round_number.desc())
            .first()
        )

    def go_to_idle(self, next_state_timestamp=None):
        previous_round = self.get_last_round()
        if not previous_round:
            Round.new(
                round_number=1,
                game=self,
                next_state_timestamp=next_state_timestamp,
            )
        else:
            Round.new(
                game=self,
                round_number=previous_round.round_number + 1,
                next_state_timestamp=next_state_timestamp,
            )
        # default to idle so no need
        # Round.update_state(round_id=previous_round.id, new_state=RoundStates.IDLE.value)

    def go_to_bidable(self, next_state_timestamp=None):
        current_round = self.get_last_round()
        # Round.new(game=self, round_number=current_round.round_number + 1)
        current_round.update_state(RoundStates.BIDABLE, next_state_timestamp)

    def go_to_waiting(self, next_state_timestamp=None):
        current_round = self.get_last_round()
        current_round.update_state(RoundStates.WAITING, next_state_timestamp)

    def go_to_result(self, winning_slot, next_state_timestamp=None):
        current_round = self.get_last_round()
        current_round.update_winning_slot(new_winning_slot=winning_slot)
        current_round.update_state(RoundStates.RESULT, next_state_timestamp)
        current_round.update_bids_after_result()
        current_round.pay_out()
