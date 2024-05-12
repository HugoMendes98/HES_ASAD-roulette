import { Injectable } from "@angular/core";

import { ApiClient } from "./api.client";
import { BidCreateDto } from "./interfaces";

@Injectable()
export class GameApiService {
	public constructor(protected readonly client: ApiClient) {}

	public addBid(gameId: number, data: BidCreateDto) {
		return this.client.post(`/games/${gameId}/bet`, data);
	}
}
