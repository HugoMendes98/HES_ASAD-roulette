import { Component } from "@angular/core";
import { MatToolbarModule } from "@angular/material/toolbar";
import { RouterOutlet } from "@angular/router";

@Component({
	selector: "app-root",
	standalone: true,
	styleUrl: "./app.component.scss",
	templateUrl: "./app.component.html",

	imports: [MatToolbarModule, RouterOutlet],
})
export class AppComponent {}
