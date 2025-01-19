import { TelegramUser } from "@/shared/types/telegram";
import { ICurrentUserResponse } from "../../types/types";

export interface IUserState {
  user: TelegramUser | null;
  currentUser: ICurrentUserResponse | null;
}
