import { getAllPacks } from "@/entities/packs/libs/packsService";
import { useActions } from "@/shared/hooks/useActions";
import { useQuery } from "@tanstack/react-query";

export const useAsyncPacks = (isAuthenticated: boolean) => {
  const { setPacks } = useActions();

  const { data, isSuccess } = useQuery({
    queryKey: ["packs"],
    queryFn: (meta) => getAllPacks(meta),
    enabled: isAuthenticated,
  });

  if (isSuccess) {
    setPacks(data);
  }
};
