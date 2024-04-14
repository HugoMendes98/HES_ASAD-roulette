import { ModuleWithProviders, NgModule } from "@angular/core";

import { API_CLIENT_CONFIG_TOKEN, ApiClient } from "./api.client";
import { GameApiService } from "./game-api.service";
import { Environment } from "../../environment";

export interface ApiModuleConfig {
	/** The configuration for the API client */
	api: Environment["api"];
}

@NgModule({ imports: [ApiClient], providers: [GameApiService] })
export class ApiModule {
	public static forRoot(
		config: ApiModuleConfig,
	): ModuleWithProviders<ApiModule> {
		return {
			ngModule: ApiModule,
			providers: [
				{ provide: API_CLIENT_CONFIG_TOKEN, useValue: config.api },
			],
		};
	}
}
