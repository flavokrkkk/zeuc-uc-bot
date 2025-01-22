import { getAllPacks } from "@/entities/packs/libs/packsService";
import { useActions } from "@/shared/hooks/useActions";
import { useQuery } from "@tanstack/react-query";

export const useAsyncPacks = () => {
  const { setPacks } = useActions();

  const { data, isSuccess } = useQuery({
    queryKey: ["packs"],
    queryFn: (meta) => getAllPacks(meta),
  });

  if (isSuccess) {
    setPacks(data);
  }
};
