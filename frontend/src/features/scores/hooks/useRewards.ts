import { getAllReward } from "@/entities/scores/libs/scoresService";
import { useActions } from "@/shared/hooks/useActions";
import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";

export const useRewards = () => {
  const { setScores } = useActions();
  const { data, isSuccess } = useQuery({
    queryKey: ["scores"],
    queryFn: (meta) => getAllReward(meta),
  });

  useEffect(() => {
    if (isSuccess && data) {
      setScores(data);
    }
  }, [isSuccess, data, setScores]);

  return { data, isSuccess };
};
