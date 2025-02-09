import { setWriteBonuses } from "@/entities/scores/libs/scoresService";
import { EBonusStatuses } from "@/entities/scores/libs/utils/rewards";
import { scoresSelectors } from "@/entities/scores/models/store/scoresSlice";
import { spinWheel } from "@/features/scores/helpers/spinWheel";
import { useActions } from "@/shared/hooks/useActions";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { useMutation } from "@tanstack/react-query";
import { useRef, useState } from "react";
import { toast } from "sonner";

export const useScopes = (
  setIsGetPrize: React.Dispatch<React.SetStateAction<boolean>>,
  setIsOpen: (action: boolean) => void,
  setPlayerId: (playerId: string) => void
) => {
  const { setCurrentUser } = useActions();
  const [spinning, setSpinning] = useState(false);
  const [winnerIndex, setWinnerIndex] = useState<number | null>(null);
  const [winner, setWinner] = useState<{
    title: string;
    reward_id: number;
    type: string;
  } | null>(null);
  const scoresValue = useAppSelector(scoresSelectors.scoresValue);

  const wheelRef = useRef<HTMLCanvasElement | null>(null);

  const onFinished = (
    winner: { title: string; reward_id: number; type: string },
    winnerIndex: number
  ) => {
    setWinnerIndex(winnerIndex);
    setWinner(winner);
    setPlayerId("");
    if (winner.type === "uc") {
      setIsOpen(true);
    }
  };

  const { mutate, isPending } = useMutation({
    mutationKey: ["scores-write"],
    mutationFn: setWriteBonuses,
    onSuccess: (data) => {
      setIsGetPrize((prev) => prev && !prev);
      setCurrentUser(data);
      spinWheel(
        scoresValue,
        wheelRef,
        spinning,
        onFinished,
        setSpinning,
        setWinnerIndex
      );
      toast.info("Бонусы списаны", {
        position: "top-center",
      });
    },
  });

  const handleScoresMutation = () => {
    mutate({ amount: 100, status: EBonusStatuses.USE });
  };

  return {
    winner,
    scores: scoresValue,
    spinning,
    wheelRef,
    winnerIndex,
    isLoading: isPending,
    calcSpinWheel: handleScoresMutation,
  };
};
