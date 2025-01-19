import { Link } from "react-router-dom";
import "./styles.css";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import Wheel from "@/shared/ui/scores/scores";
import { useScopes } from "@/features/scores/hooks/useScores";

const ScoresPage = () => {
  const { winner, scores, spinning, wheelRef, winnerIndex, calcSpinWheel } =
    useScopes();

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
        segments={scores}
        spinning={spinning}
        spinWheel={calcSpinWheel}
        winnerIndex={winnerIndex}
        wheelRef={wheelRef}
      />
    </div>
  );
};

export default ScoresPage;
