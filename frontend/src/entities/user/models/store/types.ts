import { TelegramUser } from "@/shared/types/telegram";
import {
  ICurrentUserResponse,
  IUserBonusesHistory,
  IUserDiscount,
  IUserPurchases,
} from "../../types/types";

export interface IUserState {
  user: TelegramUser | null;
  currentUser: ICurrentUserResponse | null;
  userDiscount: Array<IUserDiscount>;
  userPaymentHistory: Array<IUserPurchases>;
  userBonusesHistory: Array<IUserBonusesHistory>;
}
