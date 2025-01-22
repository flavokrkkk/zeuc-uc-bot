import { TelegramUser } from "@/shared/types/telegram";
import {
  ICurrentUserResponse,
  IUserBonusesHistory,
  IUserDiscount,
  IUserPurchases,
  IUserResponse,
} from "../types/types";
import { axiosAuth, axiosNoAuth } from "@/shared/api/baseQueryInstance";
import { EUserEndpoints } from "./utils/endpoints";
import { IQueryMetadata } from "@/shared/api/types";

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
  ): Promise<Array<IUserPurchases>> {
    const { data } = await axiosAuth.get<Array<IUserPurchases>>(
      EUserEndpoints.GET_PURCHASES,
      {
        signal: meta.signal,
      }
    );
    return data;
  }

  public async getBonusesHistory(
    meta: IQueryMetadata
  ): Promise<Array<IUserBonusesHistory>> {
    const { data } = await axiosAuth.get<Array<IUserBonusesHistory>>(
      EUserEndpoints.GET_BONUSES,
      {
        signal: meta.signal,
      }
    );
    return data;
  }

  public async getUserDiscount(
    meta: IQueryMetadata
  ): Promise<Array<IUserDiscount>> {
    const { data } = await axiosAuth.get<Array<IUserDiscount>>(
      EUserEndpoints.GET_DICOUNTS,
      {
        signal: meta.signal,
      }
    );
    return data;
  }
}

export const {
  setUserCredentials,
  getCurrentUser,
  getUserPurchases,
  getUserDiscount,
  getBonusesHistory,
} = UserService.getInstance();
