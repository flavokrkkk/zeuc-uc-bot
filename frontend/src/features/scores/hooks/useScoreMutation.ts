import { setScoreGift } from "@/entities/scores/libs/scoresService";
import { useMutation } from "@tanstack/react-query";
import { useState } from "react";

export const useScoreMutation = () => {
  const [isGetPrize, setIsGetPrize] = useState(false);
  const { mutate } = useMutation({
    mutationKey: ["score"],
    mutationFn: ({
      reward_id,
      player_id,
    }: {
      reward_id: number;
      player_id: number;
    }) => setScoreGift({ reward_id, player_id }),
  });

  const handleSetScoreGift = (event: React.MouseEvent<HTMLButtonElement>) => {
    if (!event.currentTarget.value) throw new Error("Invalid value!");

    mutate({ reward_id: Number(event.currentTarget.value), player_id: 111 });
    setIsGetPrize(true);
  };

  return {
    isGetPrize,
    setIsGetPrize,
    handleSetScoreGift,
  };
};
