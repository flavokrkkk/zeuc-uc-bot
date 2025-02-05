import { EPaymentMethods, IPack } from "@/entities/packs/types/types";
import { getPaymentUrl } from "@/entities/payment/libs/paymentService";
import { IPayementRequest } from "@/entities/payment/types/types";
import { socketSelectors } from "@/entities/socket/models/store/socketSlice";
import { userSelectors } from "@/entities/user/models/store/userSlice";
import { useActions } from "@/shared/hooks/useActions";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { useMutation } from "@tanstack/react-query";
import { ChangeEvent, useEffect, useMemo, useState } from "react";
import { toast } from "sonner";

export const usePaymentMutate = ({
  selectPacks,
  totalPacks,
  totalSum,
}: {
  selectPacks: Array<IPack>;
  totalSum: number;
  totalPacks: number;
}) => {
  const userDiscount = useAppSelector(userSelectors.userDiscount);
  const [discountId, setDiscountId] = useState<number>(0);
  const [playerId, setPlayerId] = useState("");
  const [playerError, setPlayerError] = useState<"success" | "error" | "">("");
  const [orderId, setOrderId] = useState("");

  const isConnected = useAppSelector(socketSelectors.isConnected);
  const { connectionSocket } = useActions();

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
    }),
    [selectPacks, totalSum, totalPacks, playerId, discountId]
  );

  const { mutate, isPending } = useMutation({
    mutationKey: ["payment", "url"],
    mutationFn: ({ paymentMethod }: { paymentMethod: EPaymentMethods }) => {
      return getPaymentUrl({ ...requestPayment, method_slug: paymentMethod });
    },
    onSuccess: (response) => {
      if (window.Telegram && window.Telegram.WebApp) {
        setOrderId(response.order_id);
        window.Telegram.WebApp.openLink(response.url);
      } else {
        setOrderId(response.order_id);
        window.location.href = response.url;
      }
    },
  });

  const handleUseDiscountId = (event: React.MouseEvent<HTMLButtonElement>) => {
    const discountId = Number(event?.currentTarget?.value);

    if (!discountId) throw new Error("Value is not a valid HTMLButtonElement!");

    const searchDiscount = userDiscount.find(
      (discount) => discount.discount.discount_id === discountId
    );
    if (searchDiscount) {
      toast.info("Вы активировали скидку", {
        position: "top-center",
        description: `${searchDiscount.discount.value}₽ скидка на покупку от ${searchDiscount.discount?.min_payment_value}₽`,
      });
      setDiscountId(searchDiscount.discount.discount_id);
    }
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
      toast.success("ID игрока подтверждено", {
        position: "top-center",
      });
      return;
    }

    toast.error("ID игрока не подтвреждено", {
      position: "top-center",
    });
    setPlayerError("error");
  };

  useEffect(() => {
    if (!isConnected && orderId) {
      connectionSocket({ order_id: orderId });
    }
  }, [isConnected, connectionSocket, orderId]);

  return {
    isPending,
    playerId,
    discountId,
    playerError,
    handleCheckId,
    handleChangeId,
    handleGetPayLink,
    handleUseDiscountId,
  };
};
