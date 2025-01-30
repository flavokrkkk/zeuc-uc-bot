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
  scoresWinner: null,
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
            return {
              title: `${score.discount?.value} скидка на покупку от ${score.discount?.min_payment_value}`,
              reward_id: score.reward_id,
            };
          }
          if (score.reward_type === ERewardTypes.UC_CODE) {
            return {
              title: `${score.uc_amount} UC`,
              reward_id: score.reward_id,
            };
          }

          return {} as { title: string; reward_id: number };
        });
        if (scoresView) {
          state.scoresValue = scoresView;
        }

        state.scores = payload ?? [];
      }
    ),
  }),
}).injectInto(rootReducer);

export const scoresActions = scoresSlice.actions;
export const scoresSelectors = scoresSlice.selectors;
