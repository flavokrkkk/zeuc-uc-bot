import { historyPayment } from "@/entities/payment/libs/utils/historyPayment.mock";
import PayCard from "./payCard";

const HistoryPayment = () => {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl">История заказов:</h1>
      <div className="space-y-2">
        {historyPayment.map((pay) => (
          <PayCard key={pay.id} pay={pay} />
        ))}
      </div>
    </div>
  );
};

export default HistoryPayment;
