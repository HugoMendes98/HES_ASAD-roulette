import { SocketIoConfig } from "ngx-socket-io";

export interface Environment {
	api: {
		/** Base url to the server api, should not end with `/` */
		url: string;
	};
	/** Configuration for the socket */
	socket: SocketIoConfig;
}
