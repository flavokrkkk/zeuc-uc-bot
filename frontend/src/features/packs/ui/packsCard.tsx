import { IPack } from "@/entities/packs/types/types";
import {
  Button,
  ButtonColors,
  ButtonRoundSizes,
  ButtonSizes,
} from "@/shared/ui/button/button";
import { IconTypes } from "@/shared/ui/icon/libs/libs";
import { Icon } from "@/shared/ui/icon/ui/icon";
import { FC } from "react";

interface IPacksCard {
  card: IPack;
  handleSelectPack: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

const PacksCard: FC<IPacksCard> = ({ card, handleSelectPack }) => {
  return (
    <div key={card.id} className="w-full space-y-1 text-white">
      <div className="h-[166px] space-y-0 bg-dark-200 px-4 justify-evenly flex-col w-full  аcursor-pointer border border-green-100 flex rounded-2xl">
        <section className="space-y-1 mb-2">
          <section className="flex justify-between items-center">
            <span className="flex items-center space-x-1">
              <h1 className="text-2xl">{card.uc_amount}</h1>
              <Icon type={IconTypes.UC_OUTLINED} />
            </span>
            <span className="flex items-center space-x-1">
              <h1 className="text-xs">20</h1>
              <Icon type={IconTypes.POINT_OUTLINED} />
            </span>
          </section>
          <p className="text-xs">{card.price_per_uc.price} рублей</p>
        </section>
        <Button
          isDisabled={!!card.multiplication_uc}
          value={card.id}
          bgColor={ButtonColors.GREEN}
          rounded={ButtonRoundSizes.ROUNDED_XL}
          size={ButtonSizes.SMALL}
          onClick={handleSelectPack}
        >
          Выбрать
        </Button>
        <span className="text-[9px] text-center">
          Вы получите бонусы при оплате через СБП
        </span>
      </div>
    </div>
  );
};

export default PacksCard;
