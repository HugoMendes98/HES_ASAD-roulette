import type { GameView } from "./game/views/game/game.view";

const GAME_ROOT_PATH = "games";
export const APP_PATHS = {
	auth: { login: "login", signup: "signup" },
	game: {
		getPath: (id: number) => `${GAME_ROOT_PATH}/${id}`,
		path: `${GAME_ROOT_PATH}/:${"gameId" satisfies keyof GameView}`,
	},
	games: {
		path: GAME_ROOT_PATH,
	},
} as const;
