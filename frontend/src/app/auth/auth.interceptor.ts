import {
	HttpContext,
	HttpContextToken,
	HttpErrorResponse,
	HttpEvent,
	HttpHandler,
	HttpInterceptor,
	HttpRequest,
	HttpStatusCode,
} from "@angular/common/http";
import { Injectable } from "@angular/core";
import { toSignal } from "@angular/core/rxjs-interop";
import { Observable, catchError, tap, throwError } from "rxjs";

import { AuthService } from "./auth.service";

const IGNORE_AUTH_REFRESH = new HttpContextToken(() => false);

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
	private readonly userState = toSignal(this.authService.userState$);
	/** Avoid refreshing the auth multiple in parallel  */
	private authRefreshing = false;

	public constructor(private readonly authService: AuthService) {}

	/** @inheritdoc */
	public intercept(
		req: HttpRequest<unknown>,
		next: HttpHandler,
	): Observable<HttpEvent<unknown>> {
		const token = this.authService.getAuthToken();
		const request = token
			? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
			: req;

		return next.handle(request).pipe(
			catchError(error => {
				if (
					this.authService.hasAuthToken() &&
					error instanceof HttpErrorResponse &&
					error.status === (HttpStatusCode.Unauthorized as number)
				) {
					this.authService.logout();
				}

				return throwError(() => error as never);
			}),

			tap(() => {
				if (
					req.context.get(IGNORE_AUTH_REFRESH) ||
					this.authRefreshing
				) {
					return;
				}

				const state = this.userState();
				if (!state || state.type === "unconnected") {
					return;
				}

				const { duration, expire_at } = state.info;
				const remaining = expire_at - Date.now();

				if (remaining < duration / 4) {
					this.authRefreshing = true;
					// Refresh the auth token if has used more than a percentage of its duration
					void this.authService
						.refreshAuth({
							context: new HttpContext().set(
								IGNORE_AUTH_REFRESH,
								true,
							),
						})
						.finally(() => (this.authRefreshing = false));
				}
			}),
		);
	}
}
