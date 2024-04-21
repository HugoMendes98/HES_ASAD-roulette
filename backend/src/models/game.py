from . import db

# IDK if this is the standard
from .round import Round

# technically represent a "table"
# maybe ad a "closed" state
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    money_made
    
    def __repr__(self):
        return '<Game %r>' % self.id

    @classmethod
    def new(cls):
        n = cls()
        db.session.add(n)
        db.session.commit()
        return n

    
    def get_last_round(self) -> Round:
        # do e check the state of the round too ?
        return self.rounds.order_by(Round.round_number.desc()).first() 


    def announce_result(self, winning_slot):
        current_round = self.get_last_round()
        Round.update_winning_slot(round_id=current_round.id, new_winning_slot=winning_slot)
        current_round.pay_out()