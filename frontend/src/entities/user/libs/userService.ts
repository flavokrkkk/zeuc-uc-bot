import { TelegramUser } from "@/shared/types/telegram";
import { ICurrentUserResponse, IUserResponse } from "../types/types";
import { axiosAuth, axiosNoAuth } from "@/shared/api/baseQueryInstance";
import { EUserEndpoints } from "./utils/endpoints";
import { IQueryMetadata } from "@/shared/api/types";

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

  public async getCurrentUser(
    meta: IQueryMetadata
  ): Promise<ICurrentUserResponse> {
    const { data } = await axiosAuth.get<ICurrentUserResponse>(
      EUserEndpoints.CURRENT_USER,
      {
        signal: meta.signal,
      }
    );
    return data;
  }
}

export const { setUserCredentials, getCurrentUser } = new UserService();
