import { setScoreGift } from "@/entities/scores/libs/scoresService";
import { scoresSelectors } from "@/entities/scores/models/store/scoresSlice";
import { useActions } from "@/shared/hooks/useActions";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { useMutation } from "@tanstack/react-query";
import { ChangeEvent, useState } from "react";
import { toast } from "sonner";

export const useScoreMutation = (setIsOpen: (action: boolean) => void) => {
  const scoresValue = useAppSelector(scoresSelectors.scoresValue);
  const [playerId, setPlayerId] = useState("");
  const [playerError, setPlayerError] = useState<"success" | "error" | "">("");
  const [winnerType, setWinnerType] = useState<"uc" | "discount" | "">("");
  const { getAsyncCurrentUser, getAsyncDiscount } = useActions();
  const [isGetPrize, setIsGetPrize] = useState(false);
  const { mutate, isPending } = useMutation({
    mutationKey: ["score"],
    mutationFn: ({
      reward_id,
      player_id,
    }: {
      reward_id: number;
      player_id: number;
    }) => setScoreGift({ reward_id, player_id }),
    onSuccess: () => {
      if (winnerType === "uc") {
        getAsyncCurrentUser();
      }

      toast.info("Выигрыш начислен", {
        position: "top-center",
      });

      if (winnerType === "discount") {
        getAsyncDiscount();
      }
    },
  });
  const handleSetScoreGift = (event: React.MouseEvent<HTMLButtonElement>) => {
    if (!event.currentTarget.value) throw new Error("Invalid value!");

    const currentGift = [...scoresValue].find(
      (scores) => scores.reward_id === Number(event.currentTarget.value)
    );
    setWinnerType(currentGift?.type as "uc" | "discount");
    mutate({
      reward_id: Number(event.currentTarget.value),
      player_id: Number(playerId),
    });

    setIsGetPrize(true);
  };

  const handleChangeId = (event: ChangeEvent<HTMLInputElement>) => {
    setPlayerId(event.target.value);
  };

  const handleCheckId = (event: React.MouseEvent<HTMLButtonElement>) => {
    if (!event.currentTarget.value)
      throw new Error("Value is not a valid HTMLButtonElement!");

    const playerId = event.currentTarget.value;

    if (playerId.length >= 9 && playerId.startsWith("5")) {
      setPlayerId(playerId);
      setIsOpen(false);
      toast.success("ID подтвержден", {
        position: "top-center",
      });
      setPlayerError("success");
      return;
    }

    setPlayerError("error");
  };

  return {
    isGetPrize,
    playerId,
    playerError,
    setPlayerId,
    handleChangeId,
    handleCheckId,
    setIsGetPrize,
    isPending,
    handleSetScoreGift,
  };
};
