from datetime import datetime
from app import db
from enum import Enum

class Slots(Enum):
    DOUBLE_ZERO = -1
    ZERO = 0
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


class RoundStates(Enum):
	BIDABLE = "bid-able", 0
	IDLE = "idle", 1
	WAITING = "waiting", 2
	RESULT = "results", 3
      
class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    state = db.Column(db.Integer, nullable=False)

    # it's deprecated, but I don't care
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # might be useless
    number = db.Column(db.Integer, nullable=False)
    game_id = db.Column(db.Integer, nullable=False)

    # let us get a list of round from game
    game = db.relationship("Game", backref="rounds")

    
    def __repr__(self):
        return '<Round %r>' % self.id