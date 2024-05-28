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

import { AuthLoginDto } from "../../../../lib/api";
import { FormControlsFrom } from "../../../../lib/forms";
import { APP_PATHS } from "../../../app.path";
import { AuthModule } from "../../auth.module";
import { AuthService } from "../../auth.service";

export interface LoginViewQuery {
	redirectUrl?: string;
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
export class LoginView implements Record<keyof LoginViewQuery, unknown> {
	/** Query param */
	public readonly redirectUrl = input.required<string | undefined>();

	protected readonly PATHS = APP_PATHS.auth;

	/** Login form */
	protected readonly form = new FormGroup<FormControlsFrom<AuthLoginDto>>({
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
		private _snackBar: MatSnackBar,
	) {}

	protected async submit() {
		if (this.form.invalid) {
			this.openSnackBar("Error: form not valid");
			return;
		}

		try {
			await this.service.login(this.form.getRawValue());
			this.openSnackBar(`Welcome ${this.form.getRawValue().username}`);
			return this.redirect(this.redirectUrl());
		} catch (error: unknown) {
			this.openSnackBar(
				error instanceof HttpErrorResponse && error.status === 401
					? "the password and/or the username is wrong"
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
