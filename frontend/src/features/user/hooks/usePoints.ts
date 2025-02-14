import { EPaymentMethods } from "@/entities/packs/types/types";
import { getPackForUser } from "@/entities/user/libs/userService";
import { IUserPackRequest } from "@/entities/user/types/types";
import { useMutation } from "@tanstack/react-query";
import { ChangeEvent, useState } from "react";

export const usePoints = () => {
  const { mutate, isPending } = useMutation({
    mutationKey: ["user points"],
    mutationFn: (request: IUserPackRequest) => getPackForUser(request),
    onSuccess: (response: string) => {
      if (window.Telegram && window.Telegram.WebApp) {
        window.Telegram.WebApp.openLink(response);
      } else {
        window.location.href = response;
      }
    },
  });

  const [points, setPoints] = useState("");

  const handleChangePoints = (event: ChangeEvent<HTMLInputElement>) => {
    if (Number(event.target.value) >= 1 || event.target.value === "") {
      setPoints(event.target.value);
    }
  };

  const handleGetPayLink = (event: React.MouseEvent<HTMLButtonElement>) => {
    if (!event.currentTarget.value)
      throw new Error("Value is not a valid HTMLButtonElement!");
    const paymentRequest: IUserPackRequest = {
      method_slug: event.currentTarget.value as EPaymentMethods,
      amount: Number(points) * 5,
      point: Number(points),
    };
    mutate(paymentRequest);
  };

  return {
    points,
    isPending,
    handleGetPayLink,
    handleChangePoints,
  };
};
