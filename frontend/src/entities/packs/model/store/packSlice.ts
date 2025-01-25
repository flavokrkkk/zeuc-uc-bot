import { rootReducer } from "@/shared/store";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { IPackState } from "./types";
import { IPack } from "../../types/types";

const initialState: IPackState = {
  isSelected: false,
  packSelects: [],
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
            state.packSelects[searchUc].total_sum +
            Number(state.packSelects[searchUc].price_per_uc.price);

          state.packSelects[searchUc].total_sum = finishPrice;

          state.packSelects[searchUc].multiplication_uc = Math.round(
            finishPrice / Number(state.packSelects[searchUc].price_per_uc.price)
          );
          state.isSelected = true;
        }

        state.selectedPacks = state.selectedPacks.map((el) => {
          if (el.id === state.packSelects[searchUc].id) {
            console.log("eee");
            return state.packSelects[searchUc];
          }
          return el;
        });

        state.totalPrice = state.packSelects.reduce((acc, item) => {
          return acc + item.total_sum;
        }, 0);
        state.totalPacks = state.packSelects.reduce((acc, item) => {
          return acc + item.multiplication_uc * item.uc_amount;
        }, 0);
      }
    ),
    setUnSelectPacks: create.reducer(
      (state, { payload }: PayloadAction<IPack["id"]>) => {
        const searchUc = state.packSelects.findIndex((uc) => uc.id === payload);

        if (~searchUc) {
          const finishPrice =
            state.packSelects[searchUc].total_sum -
            Number(state.packSelects[searchUc].price_per_uc.price);

          state.packSelects[searchUc].total_sum = finishPrice;

          state.packSelects[searchUc].multiplication_uc = Math.round(
            finishPrice / Number(state.packSelects[searchUc].price_per_uc.price)
          );
        }

        state.selectedPacks = state.selectedPacks.map((el) => {
          if (el.id === state.packSelects[searchUc].id) {
            console.log("eee");
            return state.packSelects[searchUc];
          }
          return el;
        });

        state.totalPrice = state.packSelects.reduce((acc, item) => {
          return acc + item.total_sum;
        }, 0);
        state.totalPacks = state.packSelects.reduce((acc, item) => {
          return acc + item.multiplication_uc * item.uc_amount;
        }, 0);

        if (!state.totalPrice) state.isSelected = false;
      }
    ),
    setSelectedPacks: create.reducer((state) => {
      state.selectedPacks = state.packSelects.filter(
        (el) => el.multiplication_uc
      );
    }),
    resetTotalPacks: create.reducer((state) => {
      state.totalPrice = 0;
      state.totalPacks = 0;
      state.selectedPacks = [];
      state.isSelected = false;
      state.packSelects = state.packSelects.map((item) => ({
        ...item,
        multiplication_uc: 0,
        total_sum: 0,
      }));
    }),
    setPacks: create.reducer(
      (state, { payload }: PayloadAction<Array<IPack>>) => {
        state.packSelects = payload.map((item) => {
          return {
            ...item,
            id: crypto.randomUUID(),
          };
        });
      }
    ),
  }),
}).injectInto(rootReducer);

export const packActions = packSlice.actions;
export const packSlectors = packSlice.selectors;
