import { Injectable } from "@angular/core";
import { BehaviorSubject, Observable, map } from "rxjs";

import { AuthApiService, LoginDto, SignupDto, UserDto } from "../../lib/api";

/**
 * When the user of the {@link AuthService} is connected
 */
export interface AuthUserStateConnected {
	/**
	 * The connected user
	 */
	user: UserDto;
}

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

	/**
	 * Subject for authUserState
	 */
	private readonly userState = AuthService.userState;

	public constructor(private readonly apiService: AuthApiService) {
		// This is just for type checking
		this.userState$ = this.userState;
		this.user$ = this.userState$.pipe(
			map(state => (state.type === "connected" ? state.user : null)),
		);
	}

	/**
	 * Logs a user with the given credentials
	 *
	 * @param body credentials
	 * @returns the connected user
	 */
	public login(body: LoginDto) {
		return this.apiService.login(body).then(user => {
			localStorage.setItem(AuthService.LOCAL_STORAGE_AUTH, user.username);
			this.userState.next({ type: "connected", user });

			return user;
		});
	}

	public signup(body: SignupDto) {
		// FIXME
		return this.login(body);
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
	public getProfile(auth: string) {
		// FIXME
		return this.login({ password: "", username: auth });
	}

	/**
	 * Will try to refresh the profile if theres something in the local storage
	 */
	public async refreshProfile() {
		const auth = this.getLocalStoredAuth();
		if (auth) {
			await this.getProfile(auth);
		}
	}

	private getLocalStoredAuth() {
		return localStorage.getItem(AuthService.LOCAL_STORAGE_AUTH);
	}
}
