interface GameStateBase<T> {
	id: number;
	type: T;
}

export interface GameStateIdle extends GameStateBase<"idle"> {
	// TODO
	_: never;
}

/** A `GameState` is the state of a running game (playing, waiting, ...) */
export type GameState = GameStateIdle;
export type GameStateType = GameState["type"];
