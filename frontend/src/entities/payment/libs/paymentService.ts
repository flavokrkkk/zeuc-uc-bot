import { axiosAuth } from "@/shared/api/baseQueryInstance";
import { IPayementRequest } from "../types/types";
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

  public async getPaymentUrl(requestData: Array<IPayementRequest>) {
    const { data } = await axiosAuth.post(EPaymentEndpoints.PAYMENT_URL, {
      requestData,
    });
    return data;
  }
}

export const { getPaymentUrl } = PaymentService.getInstance();
