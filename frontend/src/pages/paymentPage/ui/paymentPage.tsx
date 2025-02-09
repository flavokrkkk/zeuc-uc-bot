import { packSlectors } from "@/entities/packs/model/store/packSlice";
import { userSelectors } from "@/entities/user/models/store/userSlice";
import { usePacks } from "@/features/packs/hooks/usePacks";
import { usePaymentMutate } from "@/features/payment/hooks/usePaymentMutate";
import PaymentInfo from "@/features/payment/ui/paymentInfo";
import SearchUser from "@/features/user/ui/searchUser";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import {
  Button,
  ButtonColors,
  ButtonRoundSizes,
} from "@/shared/ui/button/button";
import { IconTypes } from "@/shared/ui/icon/libs/libs";
import { Icon } from "@/shared/ui/icon/ui/icon";
import { ChevronLeft, CreditCard } from "lucide-react";
import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

const PaymentPage = () => {
  const {
    totalPrice,
    totalPacks,
    totalDiscountPrice,
    handleSelectPack,
    handleUnSelectPack,
    handleResetTotalPacks,
  } = usePacks();

  const selectedPacks = useAppSelector(packSlectors.selectedPacks);
  const userInfo = useAppSelector(userSelectors.currentUser);

  const {
    handleGetPayLink,
    isPending,
    playerId,
    discountId,
    playerError,
    handleCheckId,
    handleChangeId,
    handleUseDiscountId,
  } = usePaymentMutate({
    selectPacks: selectedPacks,
    totalSum: totalPrice,
    totalPacks,
  });

  const navigate = useNavigate();

  useEffect(() => {
    if (!selectedPacks.length) {
      navigate(ERouteNames.CATALOG_PAGE);
    }
  }, []);

  return (
    <div className="space-y-5 text-white">
      <Link to={ERouteNames.CATALOG_PAGE} onClick={handleResetTotalPacks}>
        <div className="flex items-center">
          <span>
            <ChevronLeft />
          </span>
          <span>Назад</span>
        </div>
      </Link>
      <div className="flex justify-between">
        <h1 className="text-2xl mb-4">Ваш заказ</h1>
        <div className="flex items-center space-x-1">
          <span>{userInfo?.bonuses}</span>
          <span>
            <Icon type={IconTypes.POINT_OUTLINED} className="h-6 w-6" />
          </span>
        </div>
      </div>

      <PaymentInfo
        discountId={discountId}
        totalPacks={totalPacks}
        totalPrice={totalDiscountPrice ? totalDiscountPrice : totalPrice}
        selectedPacks={selectedPacks}
        handleUseDiscountId={handleUseDiscountId}
        handleSelectPack={handleSelectPack}
        handleUnSelectPack={handleUnSelectPack}
      />
      <section className="space-y-10">
        <SearchUser
          isLabel
          error={playerError}
          value={playerId.toString()}
          buttonText="Проверить ID"
          onClick={handleCheckId}
          onChange={handleChangeId}
          searchPlaceholder="Введите Player ID"
        />
        <div className="flex flex-col w-full space-y-4">
          <Button
            value="sbp"
            isDisabled={isPending || playerError !== "success"}
            className="h-14 w-full cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
            bgColor={ButtonColors.GREEN}
            rounded={ButtonRoundSizes.ROUNDED_XL}
            onClick={handleGetPayLink}
          >
            <span className="flex space-x-2 items-center">
              <Icon type={IconTypes.SBP_OUTLINED} />
              <span>Оплатить через СБП</span>
            </span>
          </Button>
          <Button
            value="card"
            isDisabled={isPending || playerError !== "success"}
            className="h-14 w-full cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
            bgColor={ButtonColors.GREEN}
            rounded={ButtonRoundSizes.ROUNDED_XL}
            onClick={handleGetPayLink}
          >
            <span className="flex space-x-2 items-center">
              <CreditCard />
              <span>Оплатить картой</span>
            </span>
          </Button>
        </div>
      </section>
    </div>
  );
};

export default PaymentPage;
