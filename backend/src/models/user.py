from .bid import Bid
from .db import db
from .round_info import InOutBets, RoundStates


class User(db.Model):
	listeners_update_balance = []

	@staticmethod
	def set_on_update_balance(listener):
		User.listeners_update_balance.append(listener)

	@staticmethod
	def hash_password(password_raw: str):
		# TODO: hash
		return password_raw

	id = db.Column(db.Integer, primary_key=True)

	# for now is unique
	username = db.Column(db.String(100), unique=True, nullable=False)

	# starts with 200$
	balance = db.Column(db.Integer, nullable=False, default=200.00)
	password_hash = db.Column(db.String(), nullable=False)

	def __repr__(self):
		return "<User %r>" % self.username

	# this can create a bet, update the bet value, remove the bet
	# raises error when the player has no enough money (or if the round is wrong, not bettable and so on)
	# if wager is + the player loses money, if wager is negative, user wants to get money back from bet
	def bet(self, player_bet: InOutBets, wager, game):
		if wager == 0:
			raise Exception("Wager is 0")

		# first get the current round of game:
		curent_round = game.get_last_round()

		# check if round is bidable
		if curent_round.state != RoundStates.BIDABLE.value:
			raise Exception("Round is not bidable.")

		the_bid = Bid.get_bids_from_round_with_bet(
			round=curent_round, player_bet=player_bet
		)

		is_new_bid = not the_bid  # if bet doesnt exists it is a new bet

		# if bid already exists
		if not is_new_bid:
			if the_bid.user_id != self.id:
				raise Exception("This slot is already taken by other user.")

		""" removed from now, imp
        if len(the_bid) > 1:
            raise Exception(
                "Cannot bet two or more bid from same player on  same round on same InOutBet. This is a critical error"
            )
        """

		absolute_wager = abs(wager)
		is_retrieving: bool = wager <= 0

		if is_retrieving:
			if is_new_bid:
				raise Exception("Cannot retrieve money because no bets.")

			computed_new_wager = the_bid.wager - absolute_wager
			if computed_new_wager <= 0:
				print(
					"player tried to remove more money than the bet, remove bet instead"
				)
				computed_new_wager = the_bid.wager

				# we should do these in a transaction
				Bid.delete_bid(bid_id=the_bid.id)
				# this will break if more than 9'999'999.99
				User.update_balance(
					user_id=self.id,
					new_balance=self.balance + computed_new_wager,
				)

			else:  # update with with lower value
				# we should do these in a transaction
				Bid.update_wager(
					bid_id=the_bid.id, new_wager=computed_new_wager
				)
				# this will break if more than 9'999'999.99
				User.update_balance(
					user_id=self.id, new_balance=self.balance + absolute_wager
				)

		else:  # is playing
			if self.balance - absolute_wager < 0:
				raise Exception("User has not enough money in balance.")

			# we should do these in a transaction
			if is_new_bid:
				Bid.new(
					inOutbet=player_bet,
					user=self,
					round=curent_round,
					wager=absolute_wager,
				)
			else:
				computed_new_wager = the_bid.wager + absolute_wager
				Bid.update_wager(
					bid_id=the_bid.id, new_wager=computed_new_wager
				)

			User.update_balance(
				user_id=self.id, new_balance=self.balance - absolute_wager
			)

		return Bid.get_bids_from_round_with_bet(
			round=curent_round, player_bet=player_bet
		)

	@classmethod
	def update_balance(cls, user_id, new_balance) -> bool:
		n = cls.query.get(user_id)
		if n:
			if n.balance != new_balance:
				for listener in User.listeners_update_balance:
					listener(n)

			n.balance = new_balance
			db.session.commit()
			return True
		raise Exception("User not found.")

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

	def to_json(self):
		return {
			"id": self.id,
			"username": self.username,
			"balance": self.balance,
		}
