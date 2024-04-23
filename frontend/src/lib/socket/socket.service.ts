import { Injectable } from "@angular/core";
import { Socket } from "ngx-socket-io";
import { map, merge } from "rxjs";

import { GameState } from "./states";

@Injectable()
export class SocketService {
	public readonly isConnected$ = merge(
		this.onConnect(),
		this.onDisconnect(),
	).pipe(
		map(() => (this.socket.ioSocket as { connected: boolean }).connected),
	);

	public constructor(public readonly socket: Socket) {}

	public onConnect() {
		return this.socket.fromEvent("connect");
	}

	public onDisconnect() {
		return this.socket.fromEvent("disconnect");
	}

	/**
	 * Ask the socket to re-emit the data for a given game
	 * @param gameId Of the game to refresh
	 */
	public askForRefresh(gameId: number) {
		this.socket.emit("/games/refresh", { gameId });
	}

	public onGameState$(gameId: number) {
		return this.socket.fromEvent<GameState>(`/games/${gameId}`);
	}

	/** Receive notification when the balance has changed */
	public onBalanceUpdate(userId: number) {
		return this.socket.fromEvent(`/users/${userId}/balance`);
	}
}
