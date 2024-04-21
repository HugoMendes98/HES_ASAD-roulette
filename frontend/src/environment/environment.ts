import { Environment } from "./environment.interface";

/** Default development environment */
export const environment: Environment = {
	api: { url: "http://localhost:5001" },
	socket: { url: "http://localhost:5001" },
};
