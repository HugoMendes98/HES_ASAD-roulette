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