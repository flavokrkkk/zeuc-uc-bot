import { axiosAuth } from "@/shared/api/baseQueryInstance";
import { EReferalEndpoints } from "./utils/endpoints";

class ReferalService {
  private static instance: ReferalService;

  private constructor() {}

  public static getInstance(): ReferalService {
    if (!ReferalService.instance) {
      ReferalService.instance = new ReferalService();
    }

    return ReferalService.instance;
  }

  public async setReferalCode({ referalCode }: { referalCode: string }) {
    const { data } = await axiosAuth.patch(
      `${EReferalEndpoints.SET_REFERAL_CODE}${referalCode}/activate`
    );
    return data;
  }
}

export const { setReferalCode } = ReferalService.getInstance();
