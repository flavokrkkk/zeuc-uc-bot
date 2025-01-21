import { axiosAuth } from "@/shared/api/baseQueryInstance";
import { IPaymentResponse, IPaymentWrap } from "../types/types";
import { EPaymentEndpoints } from "./utils/endpoints";

class PaymentService {
  private static instance: PaymentService;
  private constructor() {}
  public static getInstance() {
    if (!PaymentService.instance) {
      PaymentService.instance = new PaymentService();
    }

    return PaymentService.instance;
  }

  public async getPaymentUrl(
    requestData: IPaymentWrap
  ): Promise<IPaymentResponse> {
    const { data } = await axiosAuth.post<IPaymentResponse>(
      EPaymentEndpoints.PAYMENT_URL,
      {
        ...requestData,
      }
    );
    return data;
  }
}

export const { getPaymentUrl } = PaymentService.getInstance();
