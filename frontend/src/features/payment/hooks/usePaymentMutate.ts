import { IPack } from "@/entities/packs/types/types";
import { getPaymentUrl } from "@/entities/payment/libs/paymentService";
import { IPayementRequest, IPaymentWrap } from "@/entities/payment/types/types";
import { useMutation } from "@tanstack/react-query";
import { useMemo } from "react";

export const usePaymentMutate = ({
  selectPacks,
  totalPacks,
  totalSum,
}: {
  selectPacks: Array<IPack>;
  totalSum: number;
  totalPacks: number;
}) => {
  const requestPayment = useMemo(
    () => ({
      amount: totalSum,
      method_slug: "sbp" as IPaymentWrap["method_slug"],
      player_id: 111,
      uc_packs: selectPacks.reduce((acc: Array<IPayementRequest>, item) => {
        const obj: IPayementRequest = {
          code: item.code,
          count: item.multiplication_uc,
          price_per_uc: item.price_per_uc.price,
          total_sum: item.total_sum,
          uc_amount: item.uc_amount,
        };

        acc.push(obj);
        return acc;
      }, [] as Array<IPayementRequest>),
      uc_sum: totalPacks,
    }),
    [selectPacks, totalSum, totalPacks]
  );

  const { mutate, isPending } = useMutation({
    mutationKey: ["payment", "url"],
    mutationFn: () => getPaymentUrl(requestPayment),
    onSuccess: (response) => {
      window.location.href = response.url;
    },
  });

  const handleGetPayLink = () => mutate();

  return {
    isPending,
    handleGetPayLink,
  };
};
