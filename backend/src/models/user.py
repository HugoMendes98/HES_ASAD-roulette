from .bid import Bid
from .db import db
from .round_info import InOutBets, RoundStates
import hashlib, time


class User(db.Model):
    listeners_update_balance = []

    id = db.Column(db.Integer, primary_key=True)

    # for now is unique
    username = db.Column(db.String(100), unique=True, nullable=False)

    # starts with 200$
    balance = db.Column(db.Integer, nullable=False, default=200.00)
    password_hash = db.Column(db.String(), nullable=False)

    @staticmethod
    def set_on_update_balance(listener):
        User.listeners_update_balance.append(listener)

    @staticmethod
    def hash_password(password_raw: str):
        tmp_password_hash = hashlib.sha256(str.encode(password_raw)).hexdigest()
        # we simulate a slow password hash
        # time.sleep(1) #TODO put the sleep back
        return tmp_password_hash

    @classmethod
    def get_by_username(cls, username: str):
        return db.session.query(cls).filter_by(username=username).one_or_none()

    @classmethod
    def get_by_credentials(cls, username: str, password: str):
        user = User.get_by_username(username)
        # Always do the hash to avoid time attack
        password_hash = User.hash_password(password)

        if user is not None and user.password_hash == password_hash:
            return user

        return None

    @classmethod
    def get_by_id(cls, user_id):
        return db.session.query(cls).filter_by(id=user_id).one_or_none()

    @classmethod
    def new(cls, username: str, password: str):
        args = {
            "username": username,
            "password_hash": User.hash_password(password),
        }

        new_user = cls(**args)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def __repr__(self):
        return "<User %r>" % self.username

    def new_positive_bet(self, player_bet: InOutBets, wager, curent_round):
        if self.balance < wager:
            raise Exception("User has not enough money in balance.")

        Bid.new(inOutbet=player_bet, user=self, round=curent_round, wager=wager)

        self.update_balance(new_balance=self.balance - wager)

    def add_money_to_bid(self, money_to_add, bid: Bid):
        # should never occur
        if money_to_add <= 0:
            raise Exception("Is not a money addition!")

        if self.balance < money_to_add:
            raise Exception("User has not enough money in balance.")

        bid.update_wager(new_wager=bid.wager + money_to_add)

        self.update_balance(new_balance=self.balance - money_to_add)

    def sub_money_from_bid(self, negative_money, bid):
        # should never occur
        if negative_money >= 0:
            raise Exception("Is not a money substraction!")
        money_to_remove = abs(negative_money)

        if bid.wager <= money_to_remove:
            # remove bet and give money back
            print("player tried to remove more money than the bet, remove bet instead")

            Bid.delete_bid(bid_id=bid.id)
            self.update_balance(
                new_balance=self.balance + bid.wager,
            )
        else:
            bid.update_wager(new_wager=bid.wager - money_to_remove)

            self.update_balance(new_balance=self.balance + money_to_remove)

    # this can create a bet, update the bet value, remove the bet
    # raises error when the player has no enough money (or if the round is wrong, not bettable and so on)
    # if wager is + the player loses money, if wager is negative, user wants to get money back from bet
    def bet(self, player_bet: InOutBets, wager, game):
        # first get the current round of game:
        curent_round = game.get_last_round()

        # if not bidable, stop immediately, maybe move this in bet or round ??
        if curent_round.state != RoundStates.BIDABLE.value:
            raise Exception("Round is not bidable.")

        player_bid = curent_round.get_bet_on_inOutBet(
            player_bet=player_bet, player=self
        )
        # start txn
        if Bid.is_wager_positive(wager) and not player_bid:
            self.new_positive_bet(
                player_bet=player_bet, wager=wager, curent_round=curent_round
            )
        elif Bid.is_wager_positive(wager) and player_bid:
            self.add_money_to_bid(money_to_add=wager, bid=player_bid)
        elif not Bid.is_wager_positive(wager) and player_bid:
            self.sub_money_from_bid(negative_money=wager, bid=player_bid)
        else:
            raise Exception("Cannot remove money from a non existent bet.")
        # end txn
        return curent_round.get_bet_on_inOutBet(player_bet=player_bet, player=self)

    def update_balance(self, new_balance):
        if self.balance != new_balance:
            for listener in User.listeners_update_balance:
                listener(self)

        self.balance = new_balance
        db.session.commit()

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "balance": self.balance,
        }
