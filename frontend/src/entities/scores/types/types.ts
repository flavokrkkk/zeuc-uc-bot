import { ERewardTypes } from "../libs/utils/rewards";

export interface IScore {
  reward_id: number;
  reward_type: ERewardTypes;
  uc_code?: {
    value: number;
  };
  discount?: {
    discount_id: number;
    value: number;
    min_payment_value: number;
  };
}
