from datetime import datetime, timedelta
from random import randint

from .db import db
from .round import Round
from .round_info import RoundStates, Slots
from .. import config


# technically represent a "table"
# maybe ad a "closed" state
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)

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

    def state_machine(self):
        current_round = self.get_last_round()
        # "State machine"
        if RoundStates(current_round.state) == RoundStates.IDLE:
            self.go_to_bidable(
                datetime.utcnow() + timedelta(seconds=config.BIDABLE_time_s)
            )
            print("La manche est en préparation")
        elif RoundStates(current_round.state) == RoundStates.BIDABLE:
            self.go_to_waiting(
                datetime.utcnow() + timedelta(seconds=config.WAITING_time_s)
            )
            print(
                "Les paris sont fermés, les résultats sera annoncé dans quelque temps"
            )
        elif RoundStates(current_round.state) == RoundStates.WAITING:
            self.go_to_result(
                Slots(randint(0, 36)),
                datetime.utcnow() + timedelta(seconds=config.RESULTS_time_s),
            )
            print("Les résultats sont tombés")
        elif RoundStates(current_round.state) == RoundStates.RESULT:
            self.go_to_idle(datetime.utcnow() + timedelta(seconds=config.IDLE_time_s))
            print("La manche est terminée, un nouveau round va bientot commencer...")

    # This method prepare the game, either for a fresh start or after an anomaly
    # If a late round is detected, and it was not during the result states,
    # the game refunds the money and start fresh
    def init_game(self):
        # try to check if the last round is done correctly or not
        startNewIdleRound = True
        current_round = self.get_last_round()
        if current_round != None:  # if there are a round existing in the db
            next_state = current_round.next_state_timestamp
            sleep_time = (next_state - datetime.utcnow()).total_seconds()

            if sleep_time > 0:  # still on time
                startNewIdleRound = False
            else:
                print("late restart a new round")
                startNewIdleRound = True
                if current_round.state != RoundStates.RESULT:
                    # revert bet
                    print("cancel latest bet")
                    current_round.cancel_round()

        if startNewIdleRound:
            self.go_to_idle(datetime.utcnow() + timedelta(seconds=config.IDLE_time_s))

    def __repr__(self):
        return "<Game %r>" % self.id
