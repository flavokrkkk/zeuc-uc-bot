import { getAllPacks } from "@/entities/packs/libs/packsService";
import { useActions } from "@/shared/hooks/useActions";
import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";

export const useAsyncPacks = (isAuthenticated: boolean) => {
  const { setPacks } = useActions();

  const { data, isSuccess } = useQuery({
    queryKey: ["packs"],
    queryFn: (meta) => getAllPacks(meta),
    enabled: isAuthenticated,
  });

  useEffect(() => {
    if (isSuccess) {
      setPacks(data);
    }
  }, [isSuccess, data]);
};
