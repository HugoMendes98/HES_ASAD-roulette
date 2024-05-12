import { Environment } from "./environment.interface";

/** Default development environment */
export const environment: Environment = {
	api: { url: "/api" },
	socket: { url: "http://localhost:5000" },
};
