export interface IPack {
  id: string;
  code: string;
  multiplication_uc: number;
  price_per_uc: { price: number; point: number };
  point: number;
  price: number;
  total_sum: number;
  uc_amount: number;
}
