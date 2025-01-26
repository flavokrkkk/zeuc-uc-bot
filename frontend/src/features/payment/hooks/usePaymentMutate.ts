import { EPaymentMethods, IPack } from "@/entities/packs/types/types";
import { getPaymentUrl } from "@/entities/payment/libs/paymentService";
import { IPayementRequest } from "@/entities/payment/types/types";
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
      method_slug: EPaymentMethods.SBP,
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
    mutationFn: ({ paymentMethod }: { paymentMethod: EPaymentMethods }) =>
      getPaymentUrl({ ...requestPayment, method_slug: paymentMethod }),
    onSuccess: (response) => {
      window.location.href = response.url;
    },
  });

  const handleGetPayLink = (event: React.MouseEvent<HTMLButtonElement>) => {
    if (!event.currentTarget.value)
      throw new Error("Value is not a valid HTMLButtonElement!");
    mutate({ paymentMethod: event.currentTarget.value as EPaymentMethods });
  };

  return {
    isPending,
    handleGetPayLink,
  };
};
