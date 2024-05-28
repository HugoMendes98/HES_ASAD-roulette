import { CommonModule } from "@angular/common";
import { HttpErrorResponse } from "@angular/common/http";
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
import { MatSnackBar } from "@angular/material/snack-bar";
import { Router, RouterModule } from "@angular/router";

import { AuthSignupDto } from "../../../../lib/api";
import { FormControlsFrom } from "../../../../lib/forms";
import { APP_PATHS } from "../../../app.path";
import { AuthModule } from "../../auth.module";
import { AuthService } from "../../auth.service";

export interface SignUpViewQuery {
	redirectUrl?: string;
}

type FormSignup = FormGroup<
	FormControlsFrom<AuthSignupDto & { confirm: string }>
>;
@Component({
	standalone: true,
	styleUrl: "./signup.view.scss",
	templateUrl: "./signup.view.html",

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
export class SignUpView implements Record<keyof SignUpViewQuery, unknown> {
	/** Query param */
	public readonly redirectUrl = input.required<string | undefined>();

	protected readonly PATHS = APP_PATHS.auth;

	/** Login form */
	protected readonly form: FormSignup = new FormGroup({
		confirm: new FormControl("", {
			nonNullable: true,
			validators: [Validators.minLength(2), Validators.required],
		}),
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
	protected showPasswordConfirm = false;

	public constructor(
		private readonly service: AuthService,
		private readonly router: Router,
		private _snackBar: MatSnackBar,
	) {}

	protected async submit() {
		if (this.form.invalid) {
			this.openSnackBar("Error: form not valid");
			return;
		}

		const { confirm, password, username } = this.form.getRawValue();

		if (password !== confirm) {
			this.openSnackBar("Error: password not same");
			return;
		}

		try {
			await this.service.signup({ password, username });
			this.openSnackBar(`Welcome ${username}`);
			return this.redirect(this.redirectUrl());
		} catch (error: unknown) {
			this.openSnackBar(
				error instanceof HttpErrorResponse && error.status === 409
					? "User already exists"
					: "An error occurred",
			);
		}
	}

	private redirect(redirectUrl = "/") {
		return this.router.navigateByUrl(redirectUrl, { replaceUrl: true });
	}

	private openSnackBar(message: string) {
		this._snackBar.open(message, "", {
			duration: 3000,
		});
	}
}
