import { Component, OnInit } from "@angular/core";
import { MatToolbarModule } from "@angular/material/toolbar";
import { RouterOutlet } from "@angular/router";

import { AuthService } from "./auth/auth.service";
import { HeaderComponent } from "./header/header.component";

@Component({
	selector: "app-root",
	standalone: true,
	styleUrl: "./app.component.scss",
	templateUrl: "./app.component.html",

	imports: [HeaderComponent, MatToolbarModule, RouterOutlet],
})
export class AppComponent implements OnInit {
	public constructor(private readonly authService: AuthService) {}

	public ngOnInit() {
		void this.authService.refreshProfile();
	}
}
