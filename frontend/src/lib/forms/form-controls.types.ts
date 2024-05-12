import { FormControl } from "@angular/forms";

/** Transforms (on a single level) any object to its FormControls */
export type FormControlsFrom<T> = {
	[K in keyof Required<T>]: FormControl<T[K]>;
};

export type NullableFormControlsFrom<T> = {
	[K in keyof Required<T>]: FormControl<T[K] | null>;
};
