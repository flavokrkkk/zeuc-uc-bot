import { TelegramUser } from "@/shared/types/telegram";
import { ICurrentUserResponse, IUserResponse } from "../types/types";
import { axiosAuth, axiosNoAuth } from "@/shared/api/baseQueryInstance";
import { EUserEndpoints } from "./utils/endpoints";
import { IQueryMetadata } from "@/shared/api/types";
import { historyPayment } from "@/entities/payment/libs/utils/historyPayment.mock";

class UserService {
  private static instance: UserService;

  private constructor() {}

  public static getInstance(): UserService {
    if (!UserService.instance) {
      UserService.instance = new UserService();
    }

    return UserService.instance;
  }

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

  public async getUserPurchases(
    meta: IQueryMetadata
  ): Promise<typeof historyPayment> {
    const { data } = await axiosAuth.get<typeof historyPayment>(
      EUserEndpoints.GET_PURCHASES,
      {
        signal: meta.signal,
      }
    );
    return data;
  }
}

export const { setUserCredentials, getCurrentUser, getUserPurchases } =
  UserService.getInstance();
