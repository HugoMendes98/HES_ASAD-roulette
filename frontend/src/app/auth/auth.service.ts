import { Injectable } from "@angular/core";
import { BehaviorSubject, Observable, map } from "rxjs";

import {
	AuthApiService,
	AuthLoginDto,
	AuthSignupDto,
	AuthTokenResponse,
	UserDto,
} from "../../lib/api";
import { RequestOptions } from "../../lib/api/api.client";

/**
 * When the user of the {@link AuthService} is connected
 */
export type AuthUserStateConnected = AuthTokenResponse;

/**
 * When there is no connected user in {@link AuthService}
 */
export interface AuthUserStateUnconnected {
	/**
	 * The previously connected user if it has been logged out
	 */
	user?: UserDto;
}

/**
 * State of the user in {@link AuthService}
 */
export type AuthUserState =
	| (AuthUserStateConnected & { type: "connected" })
	| (AuthUserStateUnconnected & { type: "unconnected" });

@Injectable({ deps: [AuthApiService], providedIn: "root" })
export class AuthService {
	private static LOCAL_STORAGE_AUTH = "auth_id";

	private static readonly userState = new BehaviorSubject<AuthUserState>({
		type: "unconnected",
	});

	/**
	 * State of the current (possibly) connected user
	 */
	public readonly userState$: Observable<AuthUserState> &
		Pick<BehaviorSubject<AuthUserState>, "getValue">;

	/** Current connected user or null */
	public readonly user$: Observable<UserDto | null>;

	/** Subject for authUserState */
	private readonly userState = AuthService.userState;

	public constructor(private readonly apiService: AuthApiService) {
		// This is just for type checking
		this.userState$ = this.userState;
		this.user$ = this.userState$.pipe(
			map(state => (state.type === "connected" ? state.user : null)),
		);
	}

	/** Get the stored auth token */
	public getAuthToken() {
		return localStorage.getItem(AuthService.LOCAL_STORAGE_AUTH) ?? false;
	}
	/** Has a stored auth token */
	public hasAuthToken() {
		return this.getAuthToken() !== false;
	}

	/**
	 * Logs a user with the given credentials
	 *
	 * @param body credentials
	 * @returns the connected user
	 */
	public login(body: AuthLoginDto) {
		return this.apiService
			.login(body)
			.then(response => this.afterTokenResponse(response));
	}

	public signup(body: AuthSignupDto) {
		return this.apiService
			.signup(body)
			.then(response => this.afterTokenResponse(response));
	}

	public logout() {
		localStorage.removeItem(AuthService.LOCAL_STORAGE_AUTH);
		this.userState.next({ type: "unconnected" });
	}

	/**
	 * Get user profile
	 * @param auth identification
	 * @returns logged user
	 */
	public refreshProfile() {
		return this.apiService
			.getMe()
			.then(response => this.afterTokenResponse(response));
	}

	/** This will try to refresh if there is a stored auth token */
	public tryRefreshProfile() {
		if (!this.hasAuthToken()) {
			return Promise.resolve(false);
		}

		return this.refreshProfile();
	}

	/** Will refresh the auth token */
	public async refreshAuth(options?: Pick<RequestOptions, "context">) {
		return this.apiService
			.refresh(options)
			.then(response => this.afterTokenResponse(response));
	}

	private afterTokenResponse(response: AuthTokenResponse) {
		const { token, user } = response;
		console.log(response);

		localStorage.setItem(AuthService.LOCAL_STORAGE_AUTH, token);
		this.userState.next({ type: "connected", ...response });

		return user;
	}
}
