import { EPaymentMethods, IPack } from "@/entities/packs/types/types";
import { getPaymentUrl } from "@/entities/payment/libs/paymentService";
import { IPayementRequest } from "@/entities/payment/types/types";
import { useMutation } from "@tanstack/react-query";
import { ChangeEvent, useMemo, useState } from "react";

export const usePaymentMutate = ({
  selectPacks,
  totalPacks,
  totalSum,
}: {
  selectPacks: Array<IPack>;
  totalSum: number;
  totalPacks: number;
}) => {
  const [points, setPoints] = useState(0);
  const [discountId, setDiscountId] = useState<number>(0);
  const [playerId, setPlayerId] = useState("");
  const [playerError, setPlayerError] = useState<"success" | "error" | "">("");

  const requestPayment = useMemo(
    () => ({
      amount: totalSum,
      method_slug: EPaymentMethods.SBP,
      player_id: playerId,
      uc_packs: selectPacks.reduce((acc: Array<IPayementRequest>, item) => {
        const obj: IPayementRequest = {
          quantity: item.multiplication_uc,
          price_per_uc: item.price_per_uc,
          total_sum: item.total_sum,
          uc_amount: item.uc_amount,
        };
        acc.push(obj);
        return acc;
      }, [] as Array<IPayementRequest>),
      uc_sum: totalPacks,
      discount: discountId,
      points,
    }),
    [selectPacks, totalSum, totalPacks, playerId, discountId, points]
  );

  const { mutate, isPending } = useMutation({
    mutationKey: ["payment", "url"],
    mutationFn: ({ paymentMethod }: { paymentMethod: EPaymentMethods }) => {
      return getPaymentUrl({ ...requestPayment, method_slug: paymentMethod });
    },
    onSuccess: (response) => {
      window.location.href = response.url;
    },
  });

  const handleUsePoints = (event: React.MouseEvent<HTMLButtonElement>) => {
    if (!event.currentTarget.value)
      throw new Error("Value is not a valid HTMLButtonElement!");

    setPoints(Number(event.currentTarget.value));
  };

  const handleUseDiscountId = (event: React.MouseEvent<HTMLButtonElement>) => {
    if (!event.currentTarget.value)
      throw new Error("Value is not a valid HTMLButtonElement!");

    setDiscountId(Number(event?.currentTarget?.value));
  };

  const handleGetPayLink = (event: React.MouseEvent<HTMLButtonElement>) => {
    if (!event.currentTarget.value)
      throw new Error("Value is not a valid HTMLButtonElement!");
    mutate({ paymentMethod: event.currentTarget.value as EPaymentMethods });
  };

  const handleChangeId = (event: ChangeEvent<HTMLInputElement>) => {
    setPlayerId(event.target.value);
  };

  const handleCheckId = (event: React.MouseEvent<HTMLButtonElement>) => {
    if (!event.currentTarget.value)
      throw new Error("Value is not a valid HTMLButtonElement!");

    const playerId = event.currentTarget.value;

    if (playerId.length >= 9 && playerId.startsWith("5")) {
      setPlayerId(playerId);
      setPlayerError("success");
      return;
    }

    setPlayerError("error");
  };

  return {
    isPending,
    playerId,
    points,
    discountId,
    playerError,
    handleUsePoints,
    handleCheckId,
    handleChangeId,
    handleGetPayLink,
    handleUseDiscountId,
  };
};
