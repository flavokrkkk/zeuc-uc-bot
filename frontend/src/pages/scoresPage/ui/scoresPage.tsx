import { Link } from "react-router-dom";
import "./styles.css";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import Wheel from "@/shared/ui/scores/scores";
import { useScopes } from "@/features/scores/hooks/useScores";
import { useEffect } from "react";
import { axiosAuth } from "@/shared/api/baseQueryInstance";

const ScoresPage = () => {
  const segments = [
    "60 UC",
    "325 UC",
    "660 UC",
    "1200 UC",
    "1800 UC",
    "3850 UC",
    "8100 UC",
    "10200 UC",
  ];

  const { winner, spinning, wheelRef, winnerIndex, calcSpinWheel } =
    useScopes(segments);
  const handleXyi = async () => {
    const { data } = await axiosAuth.get("reward/all");
    return data;
  };

  useEffect(() => {
    handleXyi();
  }, []);

  return (
    <div className="flex relative justify-center items-center flex-col min-h-screen overflow-hidden">
      {/* пополнить баланс баллами */}
      <p>+</p>
      {/* баллы пользователя */}
      <h1 className="text-2xl mb-4">Мои баллы:</h1>
      <p>14</p>
      {winner && (
        <div className="mt-6 absolute top-0 text-xl text-green-800">
          You won: {winner}
        </div>
      )}

      <Link
        to={ERouteNames.CATALOG_PAGE}
        className="text-blue-600 hover:text-blue-800"
      >
        Назад
      </Link>

      <h1 className="text-2xl font-bold mb-10">Wheel of Fortune</h1>

      <Wheel
        segments={segments}
        spinning={spinning}
        spinWheel={calcSpinWheel}
        winnerIndex={winnerIndex}
        wheelRef={wheelRef}
      />
    </div>
  );
};

export default ScoresPage;
