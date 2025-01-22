import { getBonusesHistory } from "@/entities/user/libs/userService";
import { useActions } from "@/shared/hooks/useActions";
import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";

export const useTickets = () => {
  const { setBonusesHistory } = useActions();
  const { data, isSuccess } = useQuery({
    queryKey: ["tickets"],
    queryFn: (meta) => getBonusesHistory(meta),
  });

  useEffect(() => {
    if (isSuccess) {
      setBonusesHistory(data);
    }
  }, [isSuccess, data]);
};
