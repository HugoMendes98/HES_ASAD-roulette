from . import db

from . import Round

from . import RoundStates


# technically represent a "table"
# maybe ad a "closed" state
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Game %r>' % self.id

    @classmethod
    def new(cls):
        new_game = cls()
        db.session.add(new_game)
        db.session.commit()
        return new_game

    
    def get_last_round(self) -> Round:
        # do e check the state of the round too ?
        return self.rounds.order_by(Round.round_number.desc()).first() 


    def go_to_idle(self):
        previous_round = self.get_last_round()
        #TODO if no last round
        Round.new(game=self,round_number=previous_round.round_number + 1)
        Round.update_state(round_id=previous_round.id, new_state=RoundStates.IDLE)

    def go_to_bidable(self):
        current_round = self.get_last_round()
        Round.new(game=self,round_number=current_round.round_number + 1)

    def go_to_waiting(self):
        current_round = self.get_last_round()
        Round.update_state(round_id=current_round.id, new_state=RoundStates.WAITING)

    def go_to_result(self, winning_slot):
        current_round = self.get_last_round()
        Round.update_winning_slot(round_id=current_round.id, new_winning_slot=winning_slot)
        Round.update_state(round_id=current_round.id, new_state=RoundStates.RESULT)
        current_round.update_bids_after_result()
        current_round.pay_out()




