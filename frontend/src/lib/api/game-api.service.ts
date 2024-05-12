import { Injectable } from "@angular/core";

import { ApiClient } from "./api.client";
import { BidCreateDto, LoginDto, UserDto } from "./interfaces";

@Injectable()
export class GameApiService {
	public constructor(protected readonly client: ApiClient) {}

	public login(data: LoginDto) {
		return this.client.post<UserDto>("/games/user/login", data);
	}

	public addBid(gameId: number, data: BidCreateDto) {
		return this.client.post(`/games/${gameId}/bet`, data);
	}
}
