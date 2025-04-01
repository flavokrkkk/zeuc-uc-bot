import { TelegramUser } from "@/shared/types/telegram";
import {
  ICurrentUserResponse,
  IUserBonusesHistory,
  IUserDiscount,
  IUserPackRequest,
  IUserPurchases,
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
  ): Promise<{ iv: []; data: []; tag: [] }> {
    const { data } = await axiosNoAuth.post<{ iv: []; data: []; tag: [] }>(
      EUserEndpoints.SET_CREDENTIALS,
      { tg_id: telegramUser.id, username: telegramUser.username }
    );
    return data;
  }

  public async getCurrentUser(
    meta?: IQueryMetadata
  ): Promise<ICurrentUserResponse> {
    const { data } = await axiosAuth.get<ICurrentUserResponse>(
      EUserEndpoints.CURRENT_USER,
      {
        signal: meta && meta.signal,
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
    meta?: IQueryMetadata
  ): Promise<Array<IUserDiscount>> {
    const { data } = await axiosAuth.get<Array<IUserDiscount>>(
      EUserEndpoints.GET_DICOUNTS,
      {
        signal: meta && meta.signal,
      }
    );
    return data;
  }

  public async getPackForUser(request: IUserPackRequest): Promise<string> {
    const { data } = await axiosAuth.post<string>(
      EUserEndpoints.GET_USER_POINTS,
      {
        ...request,
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
  getPackForUser,
  getBonusesHistory,
} = UserService.getInstance();
