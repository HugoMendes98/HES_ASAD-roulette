import { CommonModule } from "@angular/common";
import { Component, OnDestroy, OnInit } from "@angular/core";
import { toSignal } from "@angular/core/rxjs-interop";
import { MatButtonModule } from "@angular/material/button";
import { MatIconModule } from "@angular/material/icon";
import { MatToolbarModule } from "@angular/material/toolbar";
import { Router, RouterModule } from "@angular/router";
import { Subscription, debounceTime, of, switchMap, tap } from "rxjs";

import { SocketModule, SocketService } from "../../lib/socket";
import { APP_PATHS } from "../app.path";
import { AuthModule } from "../auth/auth.module";
import { AuthService } from "../auth/auth.service";
import type { LoginViewQuery } from "../auth/views/login/login.view";

@Component({
	selector: "app-header",
	standalone: true,
	styleUrl: "./header.component.scss",
	templateUrl: "./header.component.html",

	imports: [
		AuthModule,
		CommonModule,
		MatButtonModule,
		MatIconModule,
		MatToolbarModule,
		RouterModule,
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

	/** Paths of the application */
	protected readonly APP_PATHS = APP_PATHS;

	private readonly subscription = new Subscription();

	public constructor(
		private readonly authService: AuthService,
		private readonly socketService: SocketService,
		private readonly router: Router,
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
							tap(
								() => void this.authService.tryRefreshProfile(),
							),
						);
					}),
				)
				.subscribe(),
		);
	}

	public ngOnDestroy() {
		this.subscription.unsubscribe();
	}

	protected goToLogin() {
		const { url } = this.router;
		const redirection = `/${APP_PATHS.auth.login}`;

		if (
			url.startsWith(redirection) ||
			url.startsWith(`/${APP_PATHS.auth.signup}`)
		) {
			return;
		}

		const queryParams: LoginViewQuery =
			url === "/" ? {} : { redirectUrl: url };
		return this.router.navigateByUrl(
			this.router.createUrlTree([redirection], { queryParams }),
		);
	}

	protected logout() {
		this.authService.logout();
	}
}
