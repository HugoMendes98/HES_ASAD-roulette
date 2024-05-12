import { Injectable } from "@angular/core";

import { ApiClient } from "./api.client";
import { LoginDto, UserDto } from "./interfaces";

@Injectable()
export class AuthApiService {
	public constructor(protected readonly client: ApiClient) {}

	public login(data: LoginDto) {
		return this.client.post<UserDto>("/auth/login", data);
	}
}
