import { IScore } from "../../types/types";

export interface IScoresState {
  scores: Array<IScore>;
  scoresValue: Array<{
    title: string;
    reward_id: number;
    type: string;
  }>;
  scoresWinner: IScore | null;
}
