import { scoresSelectors } from "@/entities/scores/models/store/scoresSlice";
import { spinWheel } from "@/features/helpers/spinWheel";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { useRef, useState } from "react";

export const useScopes = (
  setIsGetPrize: React.Dispatch<React.SetStateAction<boolean>>,
  setIsOpen: (action: boolean) => void,
  setPlayerId: (playerId: string) => void
) => {
  const [spinning, setSpinning] = useState(false);
  const [winnerIndex, setWinnerIndex] = useState<number | null>(null);
  const [winner, setWinner] = useState<{
    title: string;
    reward_id: number;
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

  const calcSpinWheel = () => {
    setIsGetPrize((prev) => prev && !prev);
    return spinWheel(
      scoresValue,
      wheelRef,
      spinning,
      onFinished,
      setSpinning,
      setWinnerIndex
    );
  };

  return {
    winner,
    scores: scoresValue,
    spinning,
    wheelRef,
    winnerIndex,
    calcSpinWheel,
  };
};
