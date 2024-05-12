import { CommonModule } from "@angular/common";
import { Component, input } from "@angular/core";
import {
	FormControl,
	FormGroup,
	FormsModule,
	ReactiveFormsModule,
	Validators,
} from "@angular/forms";
import { MatButtonModule } from "@angular/material/button";
import { MatCardModule } from "@angular/material/card";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatIconModule } from "@angular/material/icon";
import { MatInputModule } from "@angular/material/input";
import { Router, RouterModule } from "@angular/router";

import { LoginDto } from "../../../../lib/api";
import { FormControlsFrom } from "../../../../lib/forms";
import { APP_PATHS } from "../../../app.path";
import { AuthModule } from "../../auth.module";
import { AuthService } from "../../auth.service";

export interface LoginViewQuery {
	redirectUrl?: string;
}
export interface LoginViewRouteData {
	isSignup: boolean;
}

@Component({
	standalone: true,
	styleUrl: "./login.view.scss",
	templateUrl: "./login.view.html",

	imports: [
		AuthModule,
		CommonModule,
		FormsModule,
		MatCardModule,
		MatButtonModule,
		MatIconModule,
		MatFormFieldModule,
		MatInputModule,
		ReactiveFormsModule,
		RouterModule,
	],
})
export class LoginView
	implements Record<keyof (LoginViewQuery & LoginViewRouteData), unknown>
{
	/** Router Data, is it the signup page */
	public readonly isSignup = input.required<boolean>();
	/** Query param */
	public readonly redirectUrl = input.required<string | undefined>();

	protected readonly PATHS = APP_PATHS.auth;

	/** Login form */
	protected readonly form = new FormGroup<FormControlsFrom<LoginDto>>({
		password: new FormControl("", {
			nonNullable: true,
			validators: [Validators.minLength(2), Validators.required],
		}),
		username: new FormControl("", {
			nonNullable: true,
			validators: [Validators.minLength(2), Validators.required],
		}),
	});

	protected showPassword = false;

	public constructor(
		private readonly service: AuthService,
		private readonly router: Router,
	) {}

	protected async submit() {
		if (this.form.invalid) {
			return;
		}

		if (this.isSignup()) {
			await this.service.signup(this.form.getRawValue());
		} else {
			await this.service.login(this.form.getRawValue());
		}

		return this.redirect(this.redirectUrl());
	}

	private redirect(redirectUrl = "/") {
		return this.router.navigateByUrl(redirectUrl, { replaceUrl: true });
	}
}
