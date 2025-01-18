import { packSlectors } from "@/entities/packs/model/store/packSlice";
import { userSelectors } from "@/entities/user/models/store/userSlice";
import PaymentInfo from "@/features/payment/ui/paymentInfo";
import PaymentMethod from "@/features/payment/ui/paymentMethod";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import { Link } from "react-router-dom";

const PaymentPage = () => {
  const totalPacks = useAppSelector(packSlectors.totalPacks);
  const totalPrice = useAppSelector(packSlectors.totalPrice);
  const selectedPacks = useAppSelector(packSlectors.selectedPacks);
  const userInfo = useAppSelector(userSelectors.userInfo);

  return (
    <div className="space-y-5 text-white">
      <Link to={ERouteNames.CATALOG_PAGE}>Назад</Link>
      <h1 className="text-2xl mb-4">Ваш заказ:</h1>
      <PaymentInfo
        totalPacks={totalPacks}
        totalPrice={totalPrice}
        selectedPacks={selectedPacks}
        userInfo={userInfo}
      />
      <h1 className="text-2xl mb-4">Выберите способ оплаты: </h1>
      <PaymentMethod totalPrice={totalPrice} />
    </div>
  );
};

export default PaymentPage;
