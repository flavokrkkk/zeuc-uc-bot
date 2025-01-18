import { IPack } from "../../types/types";

export interface IPackState {
  isSelected: boolean;
  packSelects: Array<IPack>;
  totalPrice: number;
  totalPacks: number;
  selectedPacks: Array<IPack>;
}
