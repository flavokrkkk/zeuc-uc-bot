import { rootReducer } from "@/shared/store";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { IUcState } from "./types";
import { ucCardsMocks } from "../../libs/utils";
import { IUcCard } from "../../types/types";

const initialState: IUcState = {
  isSelected: false,
  ucSelects: ucCardsMocks,
  totalPrice: 0,
  totalUc: 0,
};

export const ucSlice = createSlice({
  name: "ucSlice",
  initialState,
  selectors: {
    getUcSelects: (state) => state.ucSelects,
    isSelected: (state) => state.isSelected,
    totalPrice: (state) => state.totalPrice,
    totalUc: (state) => state.totalUc,
  },
  reducers: (create) => ({
    setSelectUc: create.reducer(
      (state, { payload }: PayloadAction<IUcCard["id"]>) => {
        const searchUc = state.ucSelects.findIndex((uc) => uc.id === payload);

        if (~searchUc) {
          const finishPrice =
            state.ucSelects[searchUc].totalSum +
            Number(state.ucSelects[searchUc].pricePerUc);

          state.ucSelects[searchUc].totalSum = finishPrice;

          state.ucSelects[searchUc].multiplicationUc = Math.round(
            finishPrice / Number(state.ucSelects[searchUc].pricePerUc)
          );
          state.isSelected = true;
        }

        state.totalPrice = state.ucSelects.reduce((acc, item) => {
          return acc + item.totalSum;
        }, 0);
        state.totalUc = state.ucSelects.reduce((acc, item) => {
          return acc + item.multiplicationUc * item.ucInitial;
        }, 0);
      }
    ),
  }),
}).injectInto(rootReducer);

export const ucActions = ucSlice.actions;
export const ucSelectors = ucSlice.selectors;
