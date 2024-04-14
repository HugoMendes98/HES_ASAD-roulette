import { CommonModule } from "@angular/common";
import { Component, input } from "@angular/core";
import { toObservable } from "@angular/core/rxjs-interop";
import { FormsModule } from "@angular/forms";
import { MatButtonModule } from "@angular/material/button";
import { MatInputModule } from "@angular/material/input";
import { switchMap } from "rxjs";

import { ApiModule, GameApiService } from "../../../../lib/api";
import { SocketModule, SocketService } from "../../../../lib/socket";

@Component({
	standalone: true,
	styleUrl: "./game.view.scss",
	templateUrl: "./game.view.html",

	imports: [
		ApiModule,
		CommonModule,
		MatButtonModule,
		MatInputModule,
		FormsModule,
		SocketModule,
	],
})
export class GameView {
	/** Id from route param */
	public readonly gameId = input.required<number, string>({
		transform: query => +query,
	});

	protected readonly gameState$ = toObservable(this.gameId).pipe(
		switchMap(id => this.socket.onGameState$(id)),
	);

	protected bet: number | null = null;

	public constructor(
		private readonly gameApi: GameApiService,
		private readonly socket: SocketService,
	) {}

	public bid() {
		if (this.bet === null) {
			return;
		}

		void this.gameApi
			.addBid(this.gameId(), { bet: this.bet })
			.then(() => (this.bet = null));
	}
}
