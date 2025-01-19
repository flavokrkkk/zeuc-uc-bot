import { getAllReward } from "@/entities/scores/libs/scoresService";
import { useActions } from "@/shared/hooks/useActions";
import { useQuery } from "@tanstack/react-query";

export const useRewards = () => {
  const { setScores } = useActions();
  const { data, isSuccess } = useQuery({
    queryKey: ["scores"],
    queryFn: (meta) => getAllReward(meta),
  });

  if (isSuccess) {
    setScores(data);
  }
};
