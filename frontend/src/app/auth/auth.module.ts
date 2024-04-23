import { NgModule } from "@angular/core";

import { AuthService } from "./auth.service";
import { ApiModule } from "../../lib/api";

@NgModule({
	imports: [ApiModule],
	providers: [AuthService],
})
export class AuthModule {}
