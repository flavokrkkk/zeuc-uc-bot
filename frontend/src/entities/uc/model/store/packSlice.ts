import { rootReducer } from "@/shared/store";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { IPackState } from "./types";
import { ucCardsMocks } from "../../libs/utils";
import { IPack } from "../../types/types";

const initialState: IPackState = {
  isSelected: false,
  packSelects: ucCardsMocks,
  selectedPacks: [],
  totalPrice: 0,
  totalPacks: 0,
};

export const packSlice = createSlice({
  name: "packSlice",
  initialState,
  selectors: {
    getPackSelects: (state) => state.packSelects,
    selectedPacks: (state) => state.selectedPacks,
    isSelected: (state) => state.isSelected,
    totalPrice: (state) => state.totalPrice,
    totalPacks: (state) => state.totalPacks,
  },
  reducers: (create) => ({
    setSelectPacks: create.reducer(
      (state, { payload }: PayloadAction<IPack["id"]>) => {
        const searchUc = state.packSelects.findIndex((uc) => uc.id === payload);

        if (~searchUc) {
          const finishPrice =
            state.packSelects[searchUc].totalSum +
            Number(state.packSelects[searchUc].pricePerUc);

          state.packSelects[searchUc].totalSum = finishPrice;

          state.packSelects[searchUc].multiplicationUc = Math.round(
            finishPrice / Number(state.packSelects[searchUc].pricePerUc)
          );
          state.isSelected = true;
        }

        state.totalPrice = state.packSelects.reduce((acc, item) => {
          return acc + item.totalSum;
        }, 0);
        state.totalPacks = state.packSelects.reduce((acc, item) => {
          return acc + item.multiplicationUc * item.ucInitial;
        }, 0);
      }
    ),
    setSelectedPacks: create.reducer((state) => {
      state.selectedPacks = state.packSelects.filter(
        (el) => el.multiplicationUc
      );
    }),
  }),
}).injectInto(rootReducer);

export const packActions = packSlice.actions;
export const packSlectors = packSlice.selectors;
