import "./styles.css";
import Wheel from "@/shared/ui/scores/scores";
import { useScopes } from "@/features/scores/hooks/useScores";
import {
  Button,
  ButtonBorderSizes,
  ButtonColors,
  ButtonRoundSizes,
} from "@/shared/ui/button/button";
import { useScoreMutation } from "@/features/scores/hooks/useScoreMutation";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { userSelectors } from "@/entities/user/models/store/userSlice";

const ScoresPage = () => {
  const { handleSetScoreGift, isGetPrize, setIsGetPrize } = useScoreMutation();
  const currentUser = useAppSelector(userSelectors.currentUser);
  const { winner, scores, spinning, wheelRef, winnerIndex, calcSpinWheel } =
    useScopes(setIsGetPrize);
  return (
    <section className="w-full text-white h-full items-center space-y-2 flex flex-col justify-center pt-8">
      <div className="flex justify-center w-full  items-center flex-col overflow-hidden pt-10">
        <Wheel
          segments={scores}
          spinning={spinning}
          winnerIndex={winnerIndex}
          wheelRef={wheelRef}
        />
      </div>
      {winner && (
        <div className="flex flex-col space-y-5 w-full">
          <section className="flex justify-between items-center">
            <h1 className="text-2xl">Ваш выигрыш</h1>
            <p>{winner.title}</p>
          </section>
          <Button
            value={String(winner.reward_id)}
            className="h-14 w-full cursor-pointer flex items-center justify-center rounded-md"
            bgColor={ButtonColors.GREEN}
            isDisabled={spinning || isGetPrize}
            rounded={ButtonRoundSizes.ROUNDED_XL}
            onClick={handleSetScoreGift}
          >
            Забрать выигрыш
          </Button>
        </div>
      )}

      <Button
        className="h-14 w-full cursor-pointer flex items-center justify-center rounded-md"
        bgColor={ButtonColors.TRANSPARENT_BLACK}
        isDisabled={spinning || (currentUser?.bonuses ?? 0) < 100}
        onClick={calcSpinWheel}
        borderSize={ButtonBorderSizes.BORDER_LG}
        rounded={ButtonRoundSizes.ROUNDED_XL}
      >
        {winner ? " Крутить снова / 100 бонусов" : " Крутить / 100 бонусов"}
      </Button>
    </section>
  );
};

export default ScoresPage;
