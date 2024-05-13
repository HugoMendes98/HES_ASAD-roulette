export interface UserDto {
	balance: number;
	id: number;
	username: string;
}

export enum InOutBets {
	ONE = 1,
	TWO = 2,
	THREE = 3,
	FOUR = 4,
	FIVE = 5,
	SIX = 6,
	SEVEN = 7,
	EIGHT = 8,
	NINE = 9,
	TEN = 10,
	ELEVEN = 11,
	TWELVE = 12,
	THIRTEEN = 13,
	FOURTEEN = 14,
	FIFTEEN = 15,
	SIXTEEN = 16,
	SEVENTEEN = 17,
	EIGHTEEN = 18,
	NINETEEN = 19,
	TWENTY = 20,
	TWENTY_ONE = 21,
	TWENTY_TWO = 22,
	TWENTY_THREE = 23,
	TWENTY_FOUR = 24,
	TWENTY_FIVE = 25,
	TWENTY_SIX = 26,
	TWENTY_SEVEN = 27,
	TWENTY_EIGHT = 28,
	TWENTY_NINE = 29,
	THIRTY = 30,
	THIRTY_ONE = 31,
	THIRTY_TWO = 32,
	THIRTY_THREE = 33,
	THIRTY_FOUR = 34,
	THIRTY_FIVE = 35,
	THIRTY_SIX = 36,
}

export interface BidCreateDto {
	position_id: InOutBets;
	username: string; // FIXME: to remove
	value: number;
}
