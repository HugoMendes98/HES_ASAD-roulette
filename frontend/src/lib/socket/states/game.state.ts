interface GameStateBase<T> {
	/** Timestamp for the next state */
	next_state_timestamp: number;
	state: T;
}

export interface GameStateIdle extends GameStateBase<"IDLE"> {
	// TODO
	_: never;
}

export interface GameBets {
	/** "Slot" played */
	inOutbet: number;
	/** User that bid */
	username: string;
	wager: number;
}

interface GameStateWithBets {
	bets: readonly GameBets[];
}

export type GameStateBidable = GameStateBase<"BIDABLE"> & GameStateWithBets;
export type GameStateWaiting = GameStateBase<"WAITING"> & GameStateWithBets;

export interface GameStateResult extends GameStateBase<"RESULT">,GameStateWithBets  {
	/** Number of the slot that wins */
	winning_slot: number;
}

/** A `GameState` is the state of a running game (playing, waiting, ...) */
export type GameState =
	| GameStateBidable
	| GameStateIdle
	| GameStateResult
	| GameStateWaiting;
export type GameStateState = GameState["state"];
