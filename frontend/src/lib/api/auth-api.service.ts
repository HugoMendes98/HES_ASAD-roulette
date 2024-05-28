import { Injectable } from "@angular/core";

import { ApiClient, RequestOptions } from "./api.client";
import { UserDto } from "./interfaces";

export interface AuthLoginDto {
	password: string;
	username: string;
}

export type AuthSignupDto = AuthLoginDto;

export interface AuthTokenResponse {
	info: {
		/** Duration in ms */
		duration: number;
		/** Timestamp */
		emitted_at: number;
		/** Timestamp */
		expire_at: number;
	};
	/** Auth token */
	token: string;
	/** The connected user */
	user: UserDto;
}

@Injectable()
export class AuthApiService {
	public constructor(protected readonly client: ApiClient) {}

	public login(data: AuthLoginDto) {
		return this.client.post<AuthTokenResponse>("/auth/login", data);
	}

	public signup(data: AuthSignupDto) {
		return this.client.post<AuthTokenResponse>("/auth/signup", data);
	}

	public refresh(options?: Pick<RequestOptions, "context">) {
		return this.client.post<AuthTokenResponse>(
			"/auth/refresh",
			undefined,
			options,
		);
	}

	public getMe() {
		return this.client.get<AuthTokenResponse>("/auth/me");
	}
}
