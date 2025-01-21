import { setReferalCode } from "@/entities/referals/libs/referalService";
import { useMutation } from "@tanstack/react-query";
import { useCallback } from "react";

export const useReferal = () => {
  const { mutate } = useMutation({
    mutationKey: ["referal", "key"],
    mutationFn: (requestData: { referalCode: string }) =>
      setReferalCode(requestData),
  });

  const handleReferalActivate = useCallback(
    (event: React.MouseEvent<HTMLButtonElement>) => {
      if (!event.currentTarget.value) throw new Error("No value!");

      mutate({ referalCode: event.currentTarget.value });
    },
    []
  );

  return {
    handleReferalActivate,
  };
};
