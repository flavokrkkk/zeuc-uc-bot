import { socketSelectors } from "@/entities/socket/models/store/socketSlice";
import { getUserPurchases } from "@/entities/user/libs/userService";
import { useActions } from "@/shared/hooks/useActions";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { useWebSocketEvents } from "@/shared/hooks/useSocketEvents";
import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";
import { toast } from "sonner";

export const useSocketConnect = () => {
  const { setPaymentHistory } = useActions();
  const { data, isSuccess } = useQuery({
    queryKey: ["history", "pay"],
    queryFn: (meta) => getUserPurchases(meta),
  });

  const isConnected = useAppSelector(socketSelectors.isConnected);
  const { connectionSocket } = useActions();

  useEffect(() => {
    if (isSuccess) {
      console.log(data);
      setPaymentHistory(data);
    }
  }, [isSuccess, data]);

  useEffect(() => {
    if (!isConnected && data) {
      if (data[0]?.internal_order_id) {
        connectionSocket({ order_id: data[0].internal_order_id });
      }
    }
  }, [isConnected, connectionSocket]);

  useWebSocketEvents(
    "purchase_status",
    (data: { message: string; event: string }) => {
      console.log(data);
      toast.info(data.message, {
        position: "top-center",
      });
    }
  );
};
