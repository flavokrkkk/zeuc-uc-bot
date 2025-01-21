export interface IUserResponse {
  access_token: string;
}

export interface ICurrentUserResponse {
  username: "string";
  tg_id: number;
  bonuses: number;
  is_admin: boolean;
}
