import { ERewardTypes } from "../libs/utils/rewards";

export interface IScore {
  reward_id: number;
  reward_type: ERewardTypes;
  uc_code?: {
    code: string;
    ucinitial: number;
    price_per_uc: number;
    total_sum: number;
    multiplication_uc: number;
  };
  discount?: {
    discount_id: number;
    value: number;
    min_payment_value: number;
  };
}
