import { IUcCard } from "../../types/types";

export interface IUcState {
  isSelected: boolean;
  ucSelects: Array<IUcCard>;
  totalPrice: number;
  totalUc: number;
}
