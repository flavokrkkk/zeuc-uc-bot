import { rootReducer } from "@/shared/store";
import {
  asyncThunkCreator,
  buildCreateSlice,
  PayloadAction,
} from "@reduxjs/toolkit";
import { IScoresState } from "./types";
import { IScore } from "../../types/types";
import { ERewardTypes } from "../../libs/utils/rewards";

const createSliceWithThunks = buildCreateSlice({
  creators: { asyncThunk: asyncThunkCreator },
});

const initialState: IScoresState = {
  scores: [],
  scoresValue: [],
};

export const scoresSlice = createSliceWithThunks({
  name: "scoresSlice",
  initialState,
  selectors: {
    scores: (state) => state.scores,
    scoresValue: (state) => state.scoresValue,
  },
  reducers: (create) => ({
    setScores: create.reducer(
      (state, { payload }: PayloadAction<Array<IScore> | undefined>) => {
        const scoresView = payload?.map((score) => {
          if (score.reward_type === ERewardTypes.DISCOUNT) {
            return `${score.discount?.value} скидка на покупку от ${score.discount?.min_payment_value}`;
          }
          if (score.reward_type === ERewardTypes.UC_CODE) {
            return `${score.uc_code?.ucinitial} UC`;
          }

          return "";
        });
        state.scoresValue = scoresView ?? [];
        state.scores = payload ?? [];
      }
    ),
  }),
}).injectInto(rootReducer);

export const scoresActions = scoresSlice.actions;
export const scoresSelectors = scoresSlice.selectors;
