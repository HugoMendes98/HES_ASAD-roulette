import { CommonModule } from "@angular/common";
import { Component } from "@angular/core";
import { toSignal } from "@angular/core/rxjs-interop";
import { FormsModule } from "@angular/forms";
import { MatButtonModule } from "@angular/material/button";
import { MatToolbarModule } from "@angular/material/toolbar";

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
		MatToolbarModule,
	],
})
export class HeaderComponent {
	protected readonly user = toSignal(this.authService.user$);

	/** Input username */
	protected username = "";

	public constructor(private readonly authService: AuthService) {}

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
