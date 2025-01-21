import { TelegramUser } from "@/shared/types/telegram";
import { ICurrentUserResponse } from "../../types/types";
import { historyPayment } from "@/entities/payment/libs/utils/historyPayment.mock";

export interface IUserState {
  user: TelegramUser | null;
  currentUser: ICurrentUserResponse | null;
  userPaymentHistory: typeof historyPayment;
}
