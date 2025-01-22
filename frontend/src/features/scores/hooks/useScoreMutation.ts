import { setScoreGift } from "@/entities/scores/libs/scoresService";
import { useMutation } from "@tanstack/react-query";

export const useScoreMutation = () => {
  const { mutate } = useMutation({
    mutationKey: ["score"],
    mutationFn: ({ reward_id }: { reward_id: number }) =>
      setScoreGift({ reward_id }),
  });

  const handleSetScoreGift = (event: React.MouseEvent<HTMLButtonElement>) => {
    if (!event.currentTarget.value) throw new Error("Invalid value!");
    mutate({ reward_id: Number(event.currentTarget.value) });
  };

  return {
    handleSetScoreGift,
  };
};
