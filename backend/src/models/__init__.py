from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from enum import Enum



def register_models(app):
    db.init_app(app)

class InOutBets(Enum):
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
    # the connected numbers are missing:
    # split, street,trio,corner/square,basket/5,line/doublestreet

def get_factor_from_InOutBets(inOutBets:InOutBets):
    if inOutBets < 37:
        return 36
    if inOutBets < 43:
        return 2
    if inOutBets < 49:
        return 3


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


from .bid import Bid
from .user import User
from .round import Round
from .game import Game
