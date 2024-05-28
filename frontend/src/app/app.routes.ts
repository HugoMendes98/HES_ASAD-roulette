import { Routes } from "@angular/router";

import { APP_PATHS } from "./app.path";

export const routes: Routes = [
	{
		loadComponent: () =>
			import("./game/views/game/game.view").then(v => v.GameView),
		path: APP_PATHS.game.path,
	},
	//{
	// loadComponent: () =>
	// 	import("./game/views/games/games.view").then(v => v.GamesView),
	// path: APP_PATHS.games.path,
	//},
	{
		loadComponent: () =>
			import("./auth/views/login/login.view").then(v => v.LoginView),
		path: APP_PATHS.auth.login,
	},
	{
		loadComponent: () =>
			import("./auth/views/signup/signup.view").then(v => v.SignUpView),
		path: APP_PATHS.auth.signup,
	},
	{
		// Should be a not found page
		path: "**",
		redirectTo: APP_PATHS.game.getPath(1),
	},
];
