export interface LoginDto {
	username: string;
}
export interface UserDto extends LoginDto {
	balance: number;
}

export interface BidCreateDto {
	position_id: number;
	username: string;
	value: number;
}
