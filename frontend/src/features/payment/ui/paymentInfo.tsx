import { IPack } from "@/entities/packs/types/types";
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
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { userSelectors } from "@/entities/user/models/store/userSlice";

interface IPaymentInfo {
  discountId: number | null;
  points: number;
  totalPacks: number;
  totalPrice: number;
  selectedPacks: Array<IPack>;
  handleUseDiscountId: (event: React.MouseEvent<HTMLButtonElement>) => void;
  handleUsePoints: (event: React.MouseEvent<HTMLButtonElement>) => void;
  handleSelectPack: (event: React.MouseEvent<HTMLButtonElement>) => void;
  handleUnSelectPack: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

const PaymentInfo: FC<IPaymentInfo> = ({
  points,
  totalPrice,
  totalPacks,
  discountId,
  selectedPacks,
  handleUseDiscountId,
  handleUsePoints,
  handleSelectPack,
  handleUnSelectPack,
}) => {
  const { setUnSelectPacks } = useActions();
  const userInfo = useAppSelector(userSelectors.currentUser);
  const userDiscount = useAppSelector(userSelectors.userDiscount);
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
            isDisabled={(userInfo?.bonuses ?? 0) <= 0 || (points ?? 0) > 0}
            className="px-4"
            rounded={ButtonRoundSizes.ROUNDED_LG}
            bgColor={ButtonColors.GREEN}
            onClick={handleUsePoints}
          >
            Использовать
          </Button>
        </div>
        {userDiscount.map((discount) => (
          <div key={discount.discount.discount_id} className="flex space-x-6">
            <div className="flex space-x-3 items-center">
              <span>
                {discount.discount.value} скидка на покупку от{" "}
                {discount.discount?.min_payment_value} рублей
              </span>
            </div>
            <Button
              value={String(discount.discount.discount_id)}
              isDisabled={
                discount.discount?.min_payment_value > totalPrice ||
                Boolean(discountId)
              }
              className="px-4"
              rounded={ButtonRoundSizes.ROUNDED_LG}
              bgColor={ButtonColors.GREEN}
              onClick={handleUseDiscountId}
            >
              Использовать
            </Button>
          </div>
        ))}
      </section>
      <hr />
    </section>
  );
};

export default PaymentInfo;
