import { CommonModule } from "@angular/common";
import { Component, OnDestroy, OnInit } from "@angular/core";
import { toSignal } from "@angular/core/rxjs-interop";
import { FormsModule } from "@angular/forms";
import { MatButtonModule } from "@angular/material/button";
import { MatIconModule } from "@angular/material/icon";
import { MatToolbarModule } from "@angular/material/toolbar";
import { Subscription, debounceTime, of, switchMap, tap } from "rxjs";

import { SocketModule, SocketService } from "../../lib/socket";
import { AuthModule } from "../auth/auth.module";
import { AuthService } from "../auth/auth.service";

@Component({
	selector: "app-header",
	standalone: true,
	styleUrl: "./header.component.scss",
	templateUrl: "./header.component.html",

	imports: [
		AuthModule,
		CommonModule,
		FormsModule,
		MatButtonModule,
		MatIconModule,
		MatToolbarModule,
		SocketModule,
	],
})
export class HeaderComponent implements OnInit, OnDestroy {
	protected readonly user = toSignal(this.authService.user$);
	protected readonly isConnected = toSignal(
		this.socketService.isConnected$.pipe(
			tap(connected => {
				if (connected) {
					void this.authService.refreshProfile();
				}
			}),
		),
	);

	/** Input username */
	protected username = "";

	private readonly subscription = new Subscription();

	public constructor(
		private readonly authService: AuthService,
		private readonly socketService: SocketService,
	) {}

	public ngOnInit() {
		this.subscription.add(
			this.authService.user$
				.pipe(
					// Update socket event if the user change
					switchMap(user => {
						if (!user) {
							return of(null);
						}

						return this.socketService.onBalanceUpdate(user.id).pipe(
							debounceTime(250),
							tap(() => void this.authService.refreshProfile()),
						);
					}),
				)
				.subscribe(),
		);
	}

	public ngOnDestroy() {
		this.subscription.unsubscribe();
	}

	public login() {
		if (!this.username) {
			return;
		}

		void this.authService
			.login({ username: this.username })
			.then(() => (this.username = ""));
	}

	public logout() {
		this.authService.logout();
	}
}
