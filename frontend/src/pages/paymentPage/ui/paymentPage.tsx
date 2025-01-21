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

  const { handleGetPayLink } = usePaymentMutate({
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
        <Button
          onClick={handleGetPayLink}
          className="h-14 w-full cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
          bgColor={ButtonColors.GREEN}
          rounded={ButtonRoundSizes.ROUNDED_XL}
        >
          Оплатить
        </Button>
      </section>
    </div>
  );
};

export default PaymentPage;
