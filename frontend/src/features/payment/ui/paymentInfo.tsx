import { IPack } from "@/entities/packs/types/types";
import { ICurrentUserResponse } from "@/entities/user/types/types";
import PacksBadge from "@/features/packs/ui/packsBadge";
import { IconTypes } from "@/shared/ui/icon/libs/libs";
import { Icon } from "@/shared/ui/icon/ui/icon";
import { FC, useCallback } from "react";
import {
  Button,
  ButtonColors,
  ButtonRoundSizes,
} from "../../../shared/ui/button/button";
import { useActions } from "@/shared/hooks/useActions";
import { useNavigate } from "react-router-dom";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";

interface IPaymentInfo {
  totalPacks: number;
  totalPrice: number;
  selectedPacks: Array<IPack>;
  userInfo: ICurrentUserResponse | null;
  handleSelectPack: (event: React.MouseEvent<HTMLButtonElement>) => void;
  handleUnSelectPack: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

const PaymentInfo: FC<IPaymentInfo> = ({
  totalPrice,
  totalPacks,
  userInfo,
  selectedPacks,
  handleSelectPack,
  handleUnSelectPack,
}) => {
  const { setUnSelectPacks } = useActions();
  const navigate = useNavigate();

  const handleDeletePack = useCallback(
    (event: React.MouseEvent<HTMLButtonElement>) => {
      if (!event.currentTarget.value) throw new Error("Not a valid value!");
      if (selectedPacks.length === 1) {
        setUnSelectPacks({ id: event.currentTarget.value, type: "total" });
        navigate(ERouteNames.CATALOG_PAGE, { replace: true });
        return;
      }
      setUnSelectPacks({ id: event.currentTarget.value, type: "total" });
    },
    [selectedPacks.length]
  );

  return (
    <section className="space-y-4">
      <section className="flex  flex-col">
        <div className="space-y-2">
          {selectedPacks.map((pack) => (
            <PacksBadge
              key={pack.id}
              pack={pack}
              handleSelectPack={handleSelectPack}
              handleUnSelectPack={handleUnSelectPack}
              handleDeletePack={handleDeletePack}
            />
          ))}
        </div>
      </section>
      <section className="flex w-full space-y-3 flex-col justify-end items-end">
        <div className="flex space-x-3 items-center">
          <span>Бонусов, при оплате через СБП: </span>
          <span>
            <Icon type={IconTypes.POINT_OUTLINED} className="h-6 w-6" />
          </span>
          <span>{userInfo?.bonuses}</span>
        </div>
        <div className="space-x-2">
          <span>Итого:</span>
          <span className="text-2xl">{`${totalPacks} UC | ${totalPrice} ₽`}</span>
        </div>
        <div className="flex space-x-6">
          <div className="flex space-x-3 items-center">
            <span>У вас есть бонусов:</span>
            <span>
              <Icon type={IconTypes.POINT_OUTLINED} className="h-6 w-6" />
            </span>
            <span>{userInfo?.bonuses}</span>
          </div>
          <Button
            value={String(userInfo?.bonuses)}
            isDisabled={(userInfo?.bonuses ?? 0) <= 0}
            className="px-4"
            rounded={ButtonRoundSizes.ROUNDED_LG}
            bgColor={ButtonColors.GREEN}
          >
            Использовать
          </Button>
        </div>
      </section>
      <hr />
    </section>
  );
};

export default PaymentInfo;
