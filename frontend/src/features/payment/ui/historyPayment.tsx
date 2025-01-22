import PayCard from "./payCard";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { userSelectors } from "@/entities/user/models/store/userSlice";

const HistoryPayment = () => {
  const userPaymentHistory = useAppSelector(userSelectors.userPaymentHistory);
  return (
    <div className="space-y-4">
      <h1 className="text-2xl">История заказов:</h1>
      <div className="space-y-2">
        {userPaymentHistory.map((pay) => (
          <PayCard key={pay.id} pay={pay} />
        ))}
      </div>
    </div>
  );
};

export default HistoryPayment;
