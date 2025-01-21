import { axiosAuth } from "@/shared/api/baseQueryInstance";
import { EScoresEndpoints } from "./utils/endpoints";
import { IQueryMetadata } from "@/shared/api/types";
import { IScore } from "../types/types";

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
}

export const { getAllReward } = ScoresService.getInstance();
