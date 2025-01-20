import { historyPayment } from "@/entities/payment/libs/utils/historyPayment.mock";
import { ChevronDown, ChevronRight } from "lucide-react";
import { FC, useState } from "react";

interface IPayCard {
  pay: (typeof historyPayment)[0];
}

const PayCard: FC<IPayCard> = ({ pay }) => {
  const [isDetail, setIsDetail] = useState(false);

  const toggleDetail = () => setIsDetail((prev) => !prev);

  return (
    <div className="flex xs:justify-between xs:space-x-3 space-y-2 xs:items-center xs:space-y-0 flex-col xs:flex-row  ">
      <div className="bg-dark-200 space-y-2 flex-col p-4 h-full px-6 w-full rounded-2xl flex justify-between">
        <section className="items-center rounded-md flex justify-between space-x-5">
          <span>{pay.paymentId}</span>
          <span onClick={toggleDetail} className="cursor-pointer">
            {isDetail ? <ChevronDown /> : <ChevronRight />}
          </span>
        </section>
        {isDetail && (
          <div className="text-xs flex flex-col space-y-1 text-gray-500">
            <div className="flex space-x-4">
              <span>Сумма заказа:</span>
              <span>
                {pay.detail.ucCost} UC | {pay.detail.price} рублей
              </span>
            </div>
            <div className="flex space-x-[26.5px]">
              <span>Дата заказа:</span> <span>{pay.detail.date}</span>
            </div>
          </div>
        )}
      </div>
      <div className="rounded-3xl bg-yellow-500 w-[78px] h-[26px] flex items-center justify-center text-xs">
        {pay.status}
      </div>
    </div>
  );
};

export default PayCard;
