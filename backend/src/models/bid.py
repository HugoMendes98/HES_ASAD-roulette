from datetime import datetime
from app import db
from enum import Enum

# IDK if this is the standart
from models.round import Round


class Bets(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11
    TWELVE = 12
    THIRTEEN = 13
    FOURTEEN = 14
    FIFTEEN = 15
    SIXTEEN = 16
    SEVENTEEN = 17
    EIGHTEEN = 18
    NINETEEN = 19
    TWENTY = 20
    TWENTY_ONE = 21
    TWENTY_TWO = 22
    TWENTY_THREE = 23
    TWENTY_FOUR = 24
    TWENTY_FIVE = 25
    TWENTY_SIX = 26
    TWENTY_SEVEN = 27
    TWENTY_EIGHT = 28
    TWENTY_NINE = 29
    THIRTY = 30
    THIRTY_ONE = 31
    THIRTY_TWO = 32
    THIRTY_THREE = 33
    THIRTY_FOUR = 34
    THIRTY_FIVE = 35
    THIRTY_SIX = 36
    HALF_ONE = 37  # 1-18
    HALF_TWO = 38  # 19-36
    EVEN = 39  # mod 2 = 0
    ODD = 40  # mod 2 = 1
    BLACK = 41  # 2-4-6-8-10-11-13-15-17-20-22-24-26-28-29-31-33-35
    RED = 42  #  1-3-5-7-9-12-14-16-18-19-21-23-25-27-30-32-34-36
    THIRD_ONE = 43  # 1-12
    THIRD_TWO = 44  # 13-24
    THIRD_THREE = 45  # 25-36
    ROW_ONE = 46  # mod 3 = 1
    ROW_TWO = 47  # mod 3 = 2
    ROW_THREE = 48  # mod 3 = 0


class Bid(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # it's deprecated, but I don't care
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # max is 9'999'999.99
    wager = db.Column(db.Numeric(10, 2), nullable=False, default=10.0)

    #is the value of the enum
    bet = db.Column(db.Integer, nullable=False)

    # is null when not decided true if won, false if lost
    is_won = db.Column(db.Boolean, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    round_id = db.Column(db.Integer, db.ForeignKey("round.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)

    # let us get a list of bids from user
    user = db.relationship("User", backref="bids")
    # let us get a list of bids from round
    round = db.relationship("Round", backref="bids")
    # let us get a list of bids from game
    round = db.relationship("Game", backref="bids")

    def __repr__(self):
        return "<Bid %r>" % self.id

    @classmethod
    def new(cls, wager, bet, user_id, round_id):
        n = cls(wager=wager, bet=bet, user_id=user_id, round_id=round_id, game_id=Round.get())
        db.session.add(n)
        db.session.commit()
        return n

    @classmethod
    def get_bids_from_user_and_round(cls,user_id,round_id):
        n = db.session.query(Bid).filter_by(user_id=user_id, round_id=round_id).all()
        return n

    @classmethod
    def get_bids_from_user_and_round(cls,user_id,round_id):
        n = db.session.query(Bid).filter_by(user_id=user_id, round_id=round_id).all()
        return n
    
    @classmethod
    def get_bids_from_user(cls,user_id):
        n = db.session.query(Bid).filter_by(user_id=user_id).all()
        return n

    @classmethod
    def get_bids_from_round(cls,round_id):
        n = db.session.query(Bid).filter_by(round_id=round_id).all()
        return n

    # It is possible to have multiple winning bids (red + even),(player 1 + player 2)
    @classmethod
    def get_winning_bids_from_round(cls,round_id):
        n = db.session.query(Bid).filter_by(round_id=round_id,is_won=True).all()
        return n

    # if more specifif getter ar needed, just add them
