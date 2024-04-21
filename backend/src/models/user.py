from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # for now is unique
    username = db.Column(db.String(100), unique=True, nullable=False)

    # starts with 200$
    balance = db.Column(db.Numeric(10, 2), nullable=False, default=200.00) 
    password_hash = db.Column(db.String(64), nullable=False, default='placehodlerForSLOWHash')
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    @classmethod
    def get(cls, username):
        return db.session.query(cls).filter_by(username=username).one_or_none()
    

    @classmethod
    def new(cls, username, password_hash=None):
        args = {"username": username}
        if password_hash is not None:
            args["password_hash"] = password_hash
        new_user = cls(**args)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    