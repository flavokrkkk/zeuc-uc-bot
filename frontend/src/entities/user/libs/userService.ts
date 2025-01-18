import { TelegramUser } from "@/shared/types/telegram";
import { IUserResponse } from "../types/types";
import { axiosNoAuth } from "@/shared/api/baseQueryInstance";
import { EUserEndpoints } from "./utils/endpoints";

class UserService {
  public async setUserCredentials(
    telegramUser: TelegramUser
  ): Promise<IUserResponse> {
    const { data } = await axiosNoAuth.post<IUserResponse>(
      EUserEndpoints.SET_CREDENTIALS,
      { tg_id: telegramUser.id, username: telegramUser.username }
    );
    return data;
  }
}

export const { setUserCredentials } = new UserService();
