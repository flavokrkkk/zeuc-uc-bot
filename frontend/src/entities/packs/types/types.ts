export type PaymentMethod = { price: number; point: number };

export const enum EPaymentMethods {
  CARD = "card",
  SBP = "sbp",
}

export interface IPack {
  id: string;
  multiplication_uc: number;
  price_per_uc: number;
  quantity: number;
  total_sum: number;
  point: number;
  uc_amount: number;
}
