import { axiosAuth } from "@/shared/api/baseQueryInstance";
import { EScoresEndpoints } from "./utils/endpoints";
import { IQueryMetadata } from "@/shared/api/types";
import { IScore } from "../types/types";

class ScoresService {
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

export const { getAllReward } = new ScoresService();
