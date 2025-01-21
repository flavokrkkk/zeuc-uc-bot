import { IPack } from "@/entities/packs/types/types";
import { getPaymentUrl } from "@/entities/payment/libs/paymentService";
import { IPayementRequest } from "@/entities/payment/types/types";
import { useMutation } from "@tanstack/react-query";

export const usePaymentMutate = (
  selectPacks: Array<IPack>,
  totalSum: number
) => {
  // const {} = useMutation({
  //     mutationKey: ['payment', 'url']
  //     mutationFn: getPaymentUrl(selectPacks)
  // })
};
