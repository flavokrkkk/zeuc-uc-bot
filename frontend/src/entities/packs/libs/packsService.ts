import { axiosAuth } from "@/shared/api/baseQueryInstance";
import { EPacksEndpoints } from "./utils/endpoints";
import { IQueryMetadata } from "@/shared/api/types";
import { IPack } from "../types/types";

class PacksService {
  private static instance: PacksService;
  private constructor() {}

  public static getInstance() {
    if (!PacksService.instance) {
      PacksService.instance = new PacksService();
    }

    return PacksService.instance;
  }

  public async getAllPacks(meta: IQueryMetadata): Promise<Array<IPack>> {
    const { data } = await axiosAuth.get<Array<IPack>>(
      EPacksEndpoints.ALL_PACKS,
      {
        signal: meta.signal,
      }
    );

    return data;
  }
}

export const { getAllPacks } = PacksService.getInstance();
