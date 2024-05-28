import { CommonModule } from "@angular/common";
import {
	AfterViewInit,
	Component,
	computed,
	effect,
	HostListener,
	input,
} from "@angular/core";
import { toObservable, toSignal } from "@angular/core/rxjs-interop";
import { FormsModule } from "@angular/forms";
import { MatButtonModule } from "@angular/material/button";
import { MatInputModule } from "@angular/material/input";
import $ from "jquery";
import { CountdownComponent } from "ngx-countdown";
import { switchMap } from "rxjs";

import { ApiModule, GameApiService, InOutBets } from "../../../../lib/api";
import { SocketModule, SocketService } from "../../../../lib/socket";
import { GameBet, GameStateState } from "../../../../lib/socket/states";
import { AuthModule } from "../../../auth/auth.module";
import { AuthService } from "../../../auth/auth.service";

const _window = window as never as {
	spinWheel: (slot: number) => void;
	updateBetsView: (bets: Map<unknown, unknown>, user?: string) => void;
};

declare const initWheel: () => void; //include file wheels.js

declare const initTable: () => void; //include file setupTable.js
declare const getColorOfNumber: (param: unknown) => string; //include file setupTable.js

type BetOnTable = Partial<
	Record<InOutBets, Pick<GameBet, "userId"> & { value: number }>
>;

@Component({
	standalone: true,
	styleUrl: "./game.view.scss",
	templateUrl: "./game.view.html",

	imports: [
		AuthModule,
		ApiModule,
		CommonModule,
		MatButtonModule,
		MatInputModule,
		FormsModule,
		SocketModule,
		CountdownComponent,
	],
})
export class GameView implements AfterViewInit {
	/** Id from route param */
	public readonly gameId = input.required<number, string>({
		transform: query => +query,
	});

	protected readonly gameState$ = toObservable(this.gameId).pipe(
		switchMap(id => {
			this.socket.askForRefresh(id);
			return this.socket.onGameState$(id);
		}),
	);

	protected readonly isConnected = toSignal(this.socket.isConnected$);
	protected readonly gameState = toSignal(this.gameState$);

	/** Connected (or not) current user */
	protected readonly user = toSignal(this.authService.user$);

	protected readonly betsOnTable = computed<BetOnTable>(() => {
		const state = this.gameState();

		if (!state || state.state === "IDLE") {
			//check to show result
			return {};
		}

		return Object.fromEntries(
			state.bets.map(({ inOutbet, userId, wager }) => [
				inOutbet as InOutBets,
				{ userId, value: wager },
			]),
		);
	});

	protected readonly getColorForSlot = getColorOfNumber;

	protected amountSelected = 0;

	public constructor(
		private readonly authService: AuthService,
		private readonly gameApi: GameApiService,
		private readonly socket: SocketService,
	) {
		effect(() => {
			const game = this.gameState();
			if (game && game.state === "RESULT") {
				_window.spinWheel(game.winning_slot);
			}

			this.updateView();
		});
	}

	public ngAfterViewInit(): void {
		initWheel(); //name of the function in wheels.js file
		initTable(); //name of the function in setupTable.js file
	}

	//API POST a bet for a user
	public bid(id: number, value: number) {
		const user = this.user();
		if (
			!user ||
			!this.isConnected() ||
			!this.amountSelected ||
			this.gameState()?.state !== "BIDABLE"
		) {
			// Not connected or nothing to bet
			return;
		}

		void this.gameApi.addBid(this.gameId(), {
			position_id: id,
			username: user.username,
			value: value,
		});
	}

	/** Change the chip selected by the user */
	public changeBid(value: number) {
		this.amountSelected = value;
	}

	@HostListener("mousemove", ["$event"])
	protected onMouseMove(e: MouseEvent) {
		this.updateCursorPosition(e.clientX, e.clientY);
	}

	protected displayState(state: GameStateState): string {
		switch (state) {
			case "BIDABLE":
				return "Bid";
			case "RESULT":
				return "Result";
			case "WAITING":
				return "Wait";
			case "IDLE":
				return "Preparation";
		}
	}

	protected onSlotClick(slot: InOutBets) {
		if (this.caseAvailable(slot)) {
			this.bid(slot, this.amountSelected);
		}
	}

	/**
	 * Update all chip in the views
	 */
	private updateView() {
		//Prepare the data as used (temp only work with number)
		const bets = new Map();

		for (const [el, v] of Object.entries(this.betsOnTable())) {
			bets.set(`num-${el}`, {
				htmlElement: $(`*[data-num=${el}]`)[0],
				userId: v.userId,
				value: v.value,
			});
		}

		_window.updateBetsView(bets, this.user()?.username);
	}

	// Update position of the chip selected based on the cursor position
	private updateCursorPosition(clientX: number, clientY: number) {
		const cursorElement = document.getElementById("cursorElement");
		if (!cursorElement) {
			return;
		}

		switch (this.amountSelected) {
			case 0:
				cursorElement.innerHTML = "";
				break;
			case 1:
				cursorElement.innerHTML = `<div class="chip-container"><div class="chip blue" ><span class="chipSpan">1</span></div></div>`;
				break;
			case 5:
				cursorElement.innerHTML = `<div class="chip-container"><div class="chip orange" ><span class="chipSpan">5</span></div></div>`;
				break;
			case 10:
				cursorElement.innerHTML = `<div class="chip-container"><div class="chip purple" ><span class="chipSpan">10</span></div></div>`;
				break;
			case 25:
				cursorElement.innerHTML = `<div class="chip-container"><div class="chip red" ><span class="chipSpan">25</span></div></div>`;
				break;
			case 50:
				cursorElement.innerHTML = `<div class="chip-container"><div class="chip gold" ><span class="chipSpan">50</span></div></div>`;
				break;

			default:
				break;
		}
		cursorElement.style.left = `${clientX - 10}px`; // Adjusting for element width
		cursorElement.style.top = `${clientY - 10}px`; // Adjusting for element height
	}

	private caseAvailable(number: InOutBets) {
		const bet = this.betsOnTable()[number];
		if (!bet || bet.userId === this.user()?.id) {
			return true;
		}

		// eslint-disable-next-line no-alert -- Ok for now
		alert("Case not available");
		return false;
	}
}
