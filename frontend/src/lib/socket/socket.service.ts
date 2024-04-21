import { Injectable } from "@angular/core";
import { Socket } from "ngx-socket-io";

import { GameState } from "./states";

@Injectable()
export class SocketService {
	public constructor(public readonly socket: Socket) {}

	public onGameState$(gameId: number) {
		return this.socket.fromEvent<GameState>(`/games/${gameId}`);
	}

}
