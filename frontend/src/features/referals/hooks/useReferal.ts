import { setReferalCode } from "@/entities/referals/libs/referalService";
import { useActions } from "@/shared/hooks/useActions";
import { useMutation } from "@tanstack/react-query";
import { useCallback, useState } from "react";

export const useReferal = () => {
  const { setPointsUser } = useActions();
  const [referalError, setReferalError] = useState<"success" | "error" | "">(
    ""
  );
  const { mutate } = useMutation({
    mutationKey: ["referal", "key"],
    mutationFn: (requestData: { referalCode: string }) =>
      setReferalCode(requestData),
    onSuccess: () => {
      setReferalError("success");
      setPointsUser(20);
    },
    onError: () => {
      setReferalError("error");
    },
  });

  const handleReferalActivate = useCallback(
    (event: React.MouseEvent<HTMLButtonElement>) => {
      if (!event.currentTarget.value) throw new Error("No value!");

      mutate({ referalCode: event.currentTarget.value });
    },
    []
  );

  return {
    referalError,
    handleReferalActivate,
  };
};
