import { EPaymentMethods } from "@/entities/packs/types/types";

export interface IPaymentWrap {
  amount: number;
  method_slug: EPaymentMethods;
  player_id: number;
  uc_packs: Array<IPayementRequest>;
  uc_sum: number;
}

export interface IPayementRequest {
  uc_amount: number;
  code: string;
  price_per_uc: number;
  total_sum: number;
  count: number;
}

export interface IPaymentResponse {
  url: string;
  order_id: string;
  amount: number;
  purchase: {
    tg_id: number;
    player_id: number;
    uc_sum: number;
    price: number;
    payment_id: string;
    payment_method: EPaymentMethods;
    is_paid: false;
    metadata_: {
      tg_id: number;
      uc_packs: [
        {
          uc_amount: number;
          code: string;
          price_per_uc: number;
          total_sum: number;
          count: number;
        }
      ];
    };
    status: string;
  };
}
