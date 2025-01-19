import { spinWheel } from "@/features/helpers/spinWheel";
import { useRef, useState } from "react";

export const useScopes = (segments: Array<string>) => {
  const [spinning, setSpinning] = useState(false);
  const [winnerIndex, setWinnerIndex] = useState<number | null>(null);
  const [winner, setWinner] = useState<string | null>(null);
  const wheelRef = useRef<HTMLCanvasElement | null>(null);

  const onFinished = (winner: string, winnerIndex: number) => {
    setWinnerIndex(winnerIndex);
    setWinner(winner);
  };

  const calcSpinWheel = () =>
    spinWheel(
      segments,
      wheelRef,
      spinning,
      onFinished,
      setSpinning,
      setWinnerIndex
    );

  return {
    winner,
    spinning,
    wheelRef,
    winnerIndex,
    calcSpinWheel,
  };
};
