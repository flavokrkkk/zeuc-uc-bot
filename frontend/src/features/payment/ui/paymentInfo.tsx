import { IPack } from "@/entities/packs/types/types";
import PacksBadge from "@/features/packs/ui/packsBadge";
import { TelegramUser } from "@/shared/types/telegram";
import { IconTypes } from "@/shared/ui/icon/libs/libs";
import { Icon } from "@/shared/ui/icon/ui/icon";
import { FC } from "react";

interface IPaymentInfo {
  totalPacks: number;
  totalPrice: number;
  selectedPacks: Array<IPack>;
  userInfo: TelegramUser | null;
  handleSelectPack: (event: React.MouseEvent<HTMLButtonElement>) => void;
  handleUnSelectPack: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

const PaymentInfo: FC<IPaymentInfo> = ({
  totalPrice,
  totalPacks,
  selectedPacks,
  handleSelectPack,
  handleUnSelectPack,
}) => {
  return (
    <section className="space-y-4">
      <section className="flex  flex-col">
        <div className="space-y-2">
          {selectedPacks.map((pack) => (
            <PacksBadge
              pack={pack}
              handleSelectPack={handleSelectPack}
              handleUnSelectPack={handleUnSelectPack}
            />
          ))}
        </div>
      </section>
      <section className="flex w-full space-y-2 flex-col justify-end items-end">
        <div className="flex space-x-3 items-center">
          <span>Бонусов: </span>
          <span>
            <Icon type={IconTypes.POINT_OUTLINED} className="h-6 w-6" />
          </span>
          <span>20</span>
        </div>
        <div className="space-x-2">
          <span>Итого:</span>
          <span className="text-2xl">{`${totalPacks} UC | ${totalPrice} ₽`}</span>
        </div>
      </section>
      <hr />
    </section>
  );
};

export default PaymentInfo;
