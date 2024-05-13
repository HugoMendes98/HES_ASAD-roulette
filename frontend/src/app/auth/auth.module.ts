import { HTTP_INTERCEPTORS } from "@angular/common/http";
import { NgModule } from "@angular/core";

import { AuthInterceptor } from "./auth.interceptor";
import { AuthService } from "./auth.service";
import { ApiModule } from "../../lib/api";

@NgModule({
	imports: [ApiModule],
	providers: [
		AuthService,
		{ multi: true, provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor },
	],
})
export class AuthModule {}
