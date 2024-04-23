import { CommonModule } from "@angular/common";
import { Component, input, OnInit } from "@angular/core";
import { toObservable } from "@angular/core/rxjs-interop";
import { FormsModule } from "@angular/forms";
import { MatButtonModule } from "@angular/material/button";
import { MatInputModule } from "@angular/material/input";
import $ from "jquery";
import { switchMap } from "rxjs";

import { ApiModule, GameApiService } from "../../../../lib/api";
import { SocketModule, SocketService } from "../../../../lib/socket";
import { AuthModule } from "../../../auth/auth.module";

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
	],
})
export class GameView implements OnInit {
	/** Id from route param */
	public readonly gameId = input.required<number, string>({
		transform: query => +query,
	});

	//private readonly authService: AuthService;

	//protected readonly user = authService.getProfile()

	protected readonly gameState$ = toObservable(this.gameId).pipe(
		switchMap(id => {
			return this.socket.onGameState$(id);
		}),
	);

	protected fakesBetsFromBackEnd: any = {
		"11": {
			username: "anthony",
			value: 1,
		},
		"14": {
			username: "anthony",
			value: 10,
		},
		"15": {
			username: "toto",
			value: 10,
		},
	};

	protected username = "anthony"; //username NEED TO GET FROM THE AUTH MODULE
	protected amount = 200; //money available
	public amountSelected = 0;
	public previousState = undefined;

	public constructor(
		private readonly gameApi: GameApiService,
		private readonly socket: SocketService,
	) {}
	ngOnInit(): void {
		this.setupEvent();
		const myThis = this;
		document.addEventListener("mousemove", e => {
			myThis.updateCursorPosition(e.clientX, e.clientY);
		});

		this.gameState$.subscribe((state: any) => {
			console.log("update ! someone bet something");

			this.updateView();

			if (
				this.previousState == "BIDABLE" &&
				state["state"] == "WAITING"
			) {
				_window().spinWheel(state["winning_slot"]);
				console.log("toto");
			}
			this.previousState = state["state"];
		});
	}

	//API POST a bet for a user
	public bid(id: any, value: number) {
		void this.gameApi.addBid(this.gameId(), {
			position_id: id,
			username: this.username,
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
		const valueBet = this.amountSelected;
		let title;
		if (elementClicked.dataset.num == undefined) {
			const dataSelected = elementClicked.dataset.sector.split(",");
			title = `sector-${elementClicked.dataset.sector}`;
		} else {
			title = `num-${elementClicked.dataset.num}`;
		}
		this.bid(title, valueBet);
		this.updateView();
	}

	/**
	 * Setup Event onClick on each case to allow add chip on case
	 */
	private setupEvent() {
		$(".controlls-2 table").on("mousedown", (e: { target: any }) => {
			let elementClicked = e.target;
			if (elementClicked.tagName == "SPAN") {
				elementClicked = elementClicked.parentElement;
			}

			//Need to take care of sector, multiple sector and num later
			const number = elementClicked.dataset.num;
			if (this.caseAvailable(number)) {
				this.addChip(elementClicked);
			}
		});
	}

	/**
	 * Update all chip in the views
	 */
	private updateView() {
		//Prepare the data as used (temp only work with number)
		const bets = new Map();
		for (const el of Object.keys(this.fakesBetsFromBackEnd)) {
			bets.set(`num-${el}`, {
				htmlElement: $(`*[data-num=${el}]`)[0],
				username: this.fakesBetsFromBackEnd[el].username,
				value: this.fakesBetsFromBackEnd[el].value,
			});
		}

		_window().updateBetsView(bets, this.username);
	}
	//Update positon of the chip selected based on the cursor position
	private updateCursorPosition(clientX: number, clientY: number) {
		const cursorElement: any | null =
			document.getElementById("cursorElement");
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

	private caseAvailable(number: any) {
		if (this.fakesBetsFromBackEnd[number] == undefined) {
			return true;
		} else {
			if (this.fakesBetsFromBackEnd[number].username == this.username) {
				return true;
			}
		}
		alert("Case not available");
		return false;
	}
}

function _window(): any {
	// return the global native browser window object
	return window;
}
