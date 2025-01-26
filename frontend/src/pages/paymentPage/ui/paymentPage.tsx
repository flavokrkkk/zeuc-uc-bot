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
import { CreditCard } from "lucide-react";
import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

const PaymentPage = () => {
  const {
    totalPrice,
    totalPacks,
    handleSelectPack,
    handleUnSelectPack,
    handleResetTotalPacks,
  } = usePacks();

  const selectedPacks = useAppSelector(packSlectors.selectedPacks);
  const currentUser = useAppSelector(userSelectors.currentUser);

  const { handleGetPayLink, isPending } = usePaymentMutate({
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
        Назад
      </Link>
      <h1 className="text-2xl mb-4">Ваш заказ</h1>
      <PaymentInfo
        totalPacks={totalPacks}
        totalPrice={totalPrice}
        selectedPacks={selectedPacks}
        userInfo={currentUser}
        handleSelectPack={handleSelectPack}
        handleUnSelectPack={handleUnSelectPack}
      />
      <section className="space-y-10">
        <SearchUser
          isLabel
          buttonText="Проверить ID"
          searchPlaceholder="Введите Pubg ID"
        />
        <div className="flex flex-col w-full space-y-4">
          <Button
            value="sbp"
            isDisabled={isPending}
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
            isDisabled={isPending}
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
