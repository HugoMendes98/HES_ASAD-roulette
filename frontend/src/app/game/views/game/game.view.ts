import { CommonModule } from "@angular/common";
import { Component, computed, input, OnInit } from "@angular/core";
import { toObservable, toSignal } from "@angular/core/rxjs-interop";
import { FormsModule } from "@angular/forms";
import { MatButtonModule } from "@angular/material/button";
import { MatInputModule } from "@angular/material/input";
import $ from "jquery";
import { debounceTime, switchMap, tap } from "rxjs";

import { ApiModule, GameApiService } from "../../../../lib/api";
import { SocketModule, SocketService } from "../../../../lib/socket";
import { AuthModule } from "../../../auth/auth.module";
import { AuthService } from "../../../auth/auth.service";
import { CountdownModule } from 'ngx-countdown';
import { CountdownComponent } from 'ngx-countdown';

const _window = window as never as {
	spinWheel: (slot: number) => void;
	updateBetsView: (bets: Map<unknown, unknown>, user?: string) => void;
};

declare var initWheel: any; //include file wheels.js
declare var wheel: any; //include file wheels.js
declare var initTable: any; //include file setupTable.js
declare var getColorOfNumber: any; //include file setupTable.js

type BetOnTable = Record<string, { username: string; value: number }>;

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
		CountdownComponent
	],
})
export class GameView implements OnInit {
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

		if (!state || state.state === "IDLE") { //check to show result 
			return {};
		}

		return Object.fromEntries(
			state.bets.map(({ inOutbet, username, wager }) => [
				inOutbet,
				{ username, value: wager },
			]),
		);
	});

	protected amountSelected = 0;
	protected timer = 0;
	protected state = "";
	protected history: Number[] = []

	public constructor(
		private readonly authService: AuthService,
		private readonly gameApi: GameApiService,
		private readonly socket: SocketService,
	) { }

	public ngOnInit(): void {
		this.setupEvent();

		document.addEventListener("mousemove", e => {
			this.updateCursorPosition(e.clientX, e.clientY);
		});

		this.gameState$.pipe(debounceTime(250)).subscribe(state => {
			this.updateView();

			if (state.state === "RESULT" && wheel != undefined) {
				_window.spinWheel(state.winning_slot);
			}

			this.state = state.state;
			this.timer = new Date(state.next_state_timestamp).getSeconds() - new Date().getSeconds()
			this.history = state.last_win;
			setTimeout(() => {
				this.updateHistoryColor();
			}, 200);
	

		});
	}

	public ngAfterViewInit(): void {
		new initWheel(); //name of the function in wheels.js file
		new initTable(); //name of the function in setupTable.js file
	}

	//API POST a bet for a user
	public bid(id: number, value: number) {
		const user = this.user();
		console.log(user);
		if (!user || !this.isConnected()) {
			// Not connected
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

	/**
	 * Add a chip on the view in the correct case
	 * @param elementClicked
	 * @param valueBet
	 */
	public addChip(elementClicked: {
		dataset: { num: string | undefined; sector: string };
	}) {
		if (!elementClicked.dataset.num) {
			return;
		}

		const valueBet = this.amountSelected;
		this.bid(+(elementClicked.dataset.num ?? "0"), valueBet);
		this.updateView();
	}

	/**
	 * Setup Event onClick on each case to allow add chip on case
	 */
	private setupEvent() {
		// eslint-disable-next-line @typescript-eslint/no-explicit-any -- FIXME
		$(".controlls-2 table").on("mousedown", (e: { target: any }) => {
			/* eslint-disable @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access -- FIXME */
			let elementClicked = e.target;
			if (elementClicked.tagName === "SPAN") {
				elementClicked = elementClicked.parentElement;
			}

			// Need to take care of sector, multiple sector and num later
			const number = elementClicked.dataset.num as string;
			if (this.caseAvailable(number)) {
				this.addChip(elementClicked as never);
			}
			/* eslint-enable */
		});
	}

	/**
	 * Update all chip in the views
	 */
	private updateView() {
		console.log("up view");

		//Prepare the data as used (temp only work with number)
		const bets = new Map();
		console.log(this.betsOnTable());

		for (const [el, v] of Object.entries(this.betsOnTable())) {
			bets.set(`num-${el}`, {
				htmlElement: $(`*[data-num=${el}]`)[0],
				username: v.username,
				value: v.value,
			});
		}

		_window.updateBetsView(bets, this.user()?.username);
	}

	//Update positon of the chip selected based on the cursor position
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

	private caseAvailable(number: string) {
		const betsOnTable = this.betsOnTable();
		if (
			!betsOnTable[number] ||
			betsOnTable[number].username === this.user()?.username
		) {
			return true;
		}

		// eslint-disable-next-line no-alert -- Ok for now
		alert("Case not available");
		return false;
	}

	public displayState(state: string) {
		//19 case history
		switch (state) {
			case "BIDABLE":
				return "Bid"
			case "RESULT":
				return "Result"
			case "WAITING":
				return "Wait"
			case "IDLE":
				return "Preparation"
			default:
				return "DefaultState"
		}
	}

	private updateHistoryColor() {
		document.querySelectorAll('.history .num').forEach((el) => el.classList.add(getColorOfNumber(parseInt(el.innerHTML))));
	}

}
