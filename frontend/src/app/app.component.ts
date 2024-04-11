import { Component } from "@angular/core";
import { RouterOutlet } from "@angular/router";

@Component({
	selector: "app-root",
	standalone: true,
	styleUrl: "./app.component.scss",
	templateUrl: "./app.component.html",
	
	imports: [RouterOutlet],
})
export class AppComponent {
	public title = "frontend";
}
