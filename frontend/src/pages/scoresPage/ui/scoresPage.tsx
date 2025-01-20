import "./styles.css";
import Wheel from "@/shared/ui/scores/scores";
import { useScopes } from "@/features/scores/hooks/useScores";
import {
  Button,
  ButtonBorderSizes,
  ButtonColors,
  ButtonRoundSizes,
} from "@/shared/ui/button/button";

const ScoresPage = () => {
  const { winner, scores, spinning, wheelRef, winnerIndex, calcSpinWheel } =
    useScopes();

  return (
    <section className="w-full text-white space-y-2 flex flex-col justify-between pt-8">
      <div className="flex justify-center items-center flex-col overflow-hidden pt-10">
        <Wheel
          segments={scores}
          spinning={spinning}
          winnerIndex={winnerIndex}
          wheelRef={wheelRef}
        />
      </div>
      {winner && (
        <div className="flex flex-col space-y-5">
          <section className="flex justify-between items-center">
            <h1 className="text-2xl">Ваш выигрыш</h1>
            {winner}
          </section>
          <Button
            className="h-14 w-full cursor-pointer flex items-center justify-center rounded-md"
            bgColor={ButtonColors.GREEN}
            isDisabled={spinning}
            onClick={calcSpinWheel}
            rounded={ButtonRoundSizes.ROUNDED_XL}
          >
            Забрать выигрыш
          </Button>
        </div>
      )}

      <Button
        className="h-14 w-full cursor-pointer flex items-center justify-center rounded-md"
        bgColor={ButtonColors.TRANSPARENT_BLACK}
        isDisabled={spinning}
        onClick={calcSpinWheel}
        borderSize={ButtonBorderSizes.BORDER_LG}
        rounded={ButtonRoundSizes.ROUNDED_XL}
      >
        {winner ? " Крутить снова / 60 UC" : " Крутить / 60 UC"}
      </Button>
    </section>
  );
};

export default ScoresPage;
