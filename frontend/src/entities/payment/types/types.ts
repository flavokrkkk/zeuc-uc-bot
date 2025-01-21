export interface IPaymentWrap {
  amount: number;
  method_slug: "sbp";
  player_id: 111;
  uc_packs: Array<IPayementRequest>;
}

export interface IPayementRequest {
  ucinitial: number;
  code: string;
  price_per_uc: number;
  total_sum: number;
  count: number;
}
