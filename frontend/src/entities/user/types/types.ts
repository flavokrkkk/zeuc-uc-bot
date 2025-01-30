export interface IUserResponse {
  access_token: string;
}

export interface ICurrentUserResponse {
  username: string;
  tg_id: number;
  bonuses: number;
  is_admin: boolean;
  referal_code: string;
}
export const enum EUserPurchases {
  IN_PROGRESS = "Ожидает",
  COMPLETED = "Выполнен",
  CANCELED = "Отменен",
  GET = "Получен",
  USE = "Использован",
}
export interface IUserPurchases {
  id: string;
  tg_id: number;
  player_id: number;
  internal_order_id: string;
  uc_sum: number;
  price: number;
  payment_id: string | null;
  payment_method: string | null;
  is_paid: boolean;
  status: EUserPurchases;
}

export const statusColor: Record<EUserPurchases, string> = {
  [EUserPurchases.IN_PROGRESS]: "bg-yellow-500",
  [EUserPurchases.COMPLETED]: "bg-green-300",
  [EUserPurchases.CANCELED]: "bg-red-300",
  [EUserPurchases.GET]: "bg-green-300",
  [EUserPurchases.USE]: "bg-green-300",
};

export interface IUserBonusesHistory {
  id: string;
  amount: number;
  created_at: number;
}

export interface IDiscountModel {
  discount_id: number;
  value: number;
  min_payment_value: number;
}

export interface IUserDiscount {
  count: number;
  discount: IDiscountModel;
}
