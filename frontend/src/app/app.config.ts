import { ApplicationConfig } from "@angular/core";
import { provideAnimationsAsync } from "@angular/platform-browser/animations/async";
import { provideRouter, withComponentInputBinding } from "@angular/router";

import { routes } from "./app.routes";
import { environment } from "../environment";
import { ApiModule } from "../lib/api";
import { SocketModule } from "../lib/socket";

export const appConfig: ApplicationConfig = {
	providers: [
		provideRouter(routes, withComponentInputBinding()),
		provideAnimationsAsync(),

		...(ApiModule.forRoot({ api: environment.api }).providers ?? []),
		...(SocketModule.forRoot({ socket: environment.socket }).providers ??
			[]),
	],
};
