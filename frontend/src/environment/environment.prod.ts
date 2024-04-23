import { Environment } from "./environment.interface";

const url = `${window.location.protocol}//${window.location.host}`;

/** Default production environment */
export const environment: Environment = { api: { url }, socket: { url } };
