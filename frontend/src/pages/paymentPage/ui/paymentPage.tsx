import { packSlectors } from "@/entities/packs/model/store/packSlice";
import { userSelectors } from "@/entities/user/models/store/userSlice";
import PaymentInfo from "@/features/payment/ui/paymentInfo";
import PaymentMethod from "@/features/payment/ui/paymentMethod";
import { useActions } from "@/shared/hooks/useActions";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import { useCallback } from "react";
import { Link } from "react-router-dom";

const PaymentPage = () => {
  const totalPacks = useAppSelector(packSlectors.totalPacks);
  const totalPrice = useAppSelector(packSlectors.totalPrice);
  const selectedPacks = useAppSelector(packSlectors.selectedPacks);
  const userInfo = useAppSelector(userSelectors.userInfo);
  const { resetTotalPacks, setSelectPacks, setUnSelectPacks } = useActions();

  const handleReset = () => resetTotalPacks();

  const handleSelectPack = useCallback(
    (event: React.MouseEvent<HTMLButtonElement>) => {
      if (!event.currentTarget.value) throw new Error("Invalidate id uc!");
      setSelectPacks(event.currentTarget.value);
    },
    [setSelectPacks]
  );

  const handleUnSelectPack = useCallback(
    (event: React.MouseEvent<HTMLButtonElement>) => {
      if (!event.currentTarget.value) throw new Error("Invalidate id uc!");
      setUnSelectPacks(event.currentTarget.value);
    },
    [setSelectPacks]
  );
  console.log(selectedPacks);
  return (
    <div className="space-y-5 text-white">
      <Link to={ERouteNames.CATALOG_PAGE} onClick={handleReset}>
        Назад
      </Link>
      <h1 className="text-2xl mb-4">Ваш заказ:</h1>
      <PaymentInfo
        totalPacks={totalPacks}
        totalPrice={totalPrice}
        selectedPacks={selectedPacks}
        userInfo={userInfo}
        handleSelectPack={handleSelectPack}
        handleUnSelectPack={handleUnSelectPack}
      />
      <h1 className="text-2xl mb-4">Выберите способ оплаты: </h1>
      <PaymentMethod totalPrice={totalPrice} />
    </div>
  );
};

export default PaymentPage;
