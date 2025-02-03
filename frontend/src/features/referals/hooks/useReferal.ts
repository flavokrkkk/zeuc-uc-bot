import { setReferalCode } from "@/entities/referals/libs/referalService";
import { useActions } from "@/shared/hooks/useActions";
import { useMutation } from "@tanstack/react-query";
import { useCallback, useState } from "react";
import { toast } from "sonner";

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
      toast.success("Успешно активировано!", {
        position: "top-center",
      });
    },
    onError: () => {
      setReferalError("error");
      toast.error("Не удалось активировать", {
        position: "top-center",
      });
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
