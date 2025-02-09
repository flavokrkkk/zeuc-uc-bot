import { axiosAuth } from "@/shared/api/baseQueryInstance";
import { EScoresEndpoints } from "./utils/endpoints";
import { IQueryMetadata } from "@/shared/api/types";
import { IScore } from "../types/types";
import { EBonusStatuses } from "./utils/rewards";
import { ICurrentUserResponse } from "@/entities/user/types/types";

class ScoresService {
  private static instance: ScoresService;

  private constructor() {}

  public static getInstance() {
    if (!ScoresService.instance) {
      ScoresService.instance = new ScoresService();
    }

    return ScoresService.instance;
  }

  public async getAllReward(meta: IQueryMetadata): Promise<Array<IScore>> {
    const { data } = await axiosAuth.get<Array<IScore>>(
      EScoresEndpoints.GET_SCORES,
      {
        signal: meta.signal,
      }
    );
    return data;
  }

  public async setWriteBonuses(requestBody: {
    amount: number;
    status: EBonusStatuses;
  }): Promise<ICurrentUserResponse> {
    const { data } = await axiosAuth.patch<ICurrentUserResponse>(
      EScoresEndpoints.SET_WRITE,
      requestBody
    );
    return data;
  }

  public async setScoreGift(body: { reward_id: number; player_id: number }) {
    const { data } = await axiosAuth.post(`${EScoresEndpoints.SET_GIFTS}`, {
      ...body,
    });
    return data;
  }
}

export const { getAllReward, setScoreGift, setWriteBonuses } =
  ScoresService.getInstance();
