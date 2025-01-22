import { getUserPurchases } from "@/entities/user/libs/userService";
import { useQuery } from "@tanstack/react-query";
import { useActions } from "../../../shared/hooks/useActions";

export const useHistoryPayment = () => {
  const { setPaymentHistory } = useActions();
  const { data, isSuccess } = useQuery({
    queryKey: ["history", "pay"],
    queryFn: (meta) => getUserPurchases(meta),
  });

  if (isSuccess) {
    setPaymentHistory(data);
  }
};
