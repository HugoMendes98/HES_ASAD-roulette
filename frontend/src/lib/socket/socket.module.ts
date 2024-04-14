import { ModuleWithProviders, NgModule } from "@angular/core";
import { SocketIoModule } from "ngx-socket-io";

import { SocketService } from "./socket.service";
import { Environment } from "../../environment";

export interface SocketModuleOptions {
	socket: Environment["socket"];
}

@NgModule({ providers: [SocketService] })
export class SocketModule {
	public static forRoot(
		options: SocketModuleOptions,
	): ModuleWithProviders<SocketModule> {
		const {
			socket: { options: sockOptions = {}, url },
		} = options;

		const { providers = [] } = SocketIoModule.forRoot({
			options: { autoConnect: true, reconnection: true, ...sockOptions },
			url,
		});
		return { ngModule: SocketModule, providers };
	}
}
