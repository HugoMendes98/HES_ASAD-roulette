from . import db

# technically represent a "table"
# maybe ad a "closed" state
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    def __repr__(self):
        return '<Game %r>' % self.id

    @classmethod
    def new(cls):
        n = cls()
        db.session.add(n)
        db.session.commit()
        return n

    @classmethod
    def get_bids_from_user_and_round(cls,user_id,round_id):
        n = db.session.query(Bid).filter_by(user_id=user_id, round_id=round_id).all()
        return n