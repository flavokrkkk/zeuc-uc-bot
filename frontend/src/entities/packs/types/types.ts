export type PaymentMethod = { price: number; point: number };

export const enum EPaymentMethods {
  CARD = "card",
  SBP = "sbp",
}

export interface IPack {
  id: string;
  code: string;
  multiplication_uc: number;
  price_per_uc: PaymentMethod;
  point: number;
  price: number;
  total_sum: number;
  uc_amount: number;
}
