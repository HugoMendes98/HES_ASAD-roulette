import { Injectable } from "@angular/core";

import { ApiClient } from "./api.client";

@Injectable()
export class GameApiService {
	public constructor(protected readonly client: ApiClient) {}

	public addBid(gameId: number, data: unknown) {
		// TODO
		return this.client.post(`/games/${gameId}/bet`, data);
	}
}
