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
		// Should be a not found page
		path: "**",
		redirectTo: APP_PATHS.game.getPath(1),
	},
];
