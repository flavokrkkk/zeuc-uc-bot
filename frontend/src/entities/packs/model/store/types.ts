import { IPack } from "../../types/types";

export interface IPackState {
  isSelected: boolean;
  packSelects: Array<IPack>;
  totalPrice: number;
  totalPacks: number;
  totalDiscountPrice: number;
  selectedPacks: Array<IPack>;
}
