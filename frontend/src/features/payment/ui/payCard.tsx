import { IUserPurchases, statusColor } from "@/entities/user/types/types";
import { IconTypes } from "@/shared/ui/icon/libs/libs";
import { Icon } from "@/shared/ui/icon/ui/icon";
import clsx from "clsx";
import { ChevronDown, ChevronRight } from "lucide-react";
import { FC, useState } from "react";

interface IPayCard {
  pay: IUserPurchases;
}

const PayCard: FC<IPayCard> = ({ pay }) => {
  const [isDetail, setIsDetail] = useState(false);

  const toggleDetail = () => setIsDetail((prev) => !prev);

  return (
    <div className="flex xs:justify-between xs:space-x-3 space-y-2 xs:items-center xs:space-y-0 flex-col xs:flex-row  ">
      <div className="bg-dark-200 space-y-2 flex-col p-4 h-full px-6 w-full rounded-2xl flex justify-between">
        <section className="items-center rounded-md flex justify-between space-x-5">
          <span>{pay.payment_id}</span>
          <span onClick={toggleDetail} className="cursor-pointer">
            {isDetail ? (
              <ChevronDown className="text-green-100 cursor-pointer w-7 h-7  transition-all duration-300 hover:translate-y-1 hover:text-red-400" />
            ) : (
              <ChevronRight className="text-green-100 cursor-pointer w-7 h-7 transition-all duration-300 hover:translate-x-1 hover:text-red-400" />
            )}
          </span>
        </section>
        {isDetail && (
          <div key={pay.id} className="flex justify-between  pb-2">
            <section className="flex flex-col space-y-1">
              <div className="text-sm flex space-x-2">
                <span className="font-bold text-gray-600">Количество -</span>
                <span className="flex space-x-1 items-center">
                  <span>{pay.uc_sum}</span>{" "}
                  <Icon type={IconTypes.UC_OUTLINED} className="h-5 w-5" />
                </span>
              </div>
              <div className="text-sm flex space-x-2">
                <span className="font-bold text-gray-600">Cумма заказа -</span>
                <span className="flex space-x-1 items-center">
                  {pay.price} рублей
                </span>
              </div>

              <div className="text-sm">
                <span className="font-bold text-gray-600">Дата покупки - </span>{" "}
                <span>{pay.created_at}</span>
              </div>
            </section>
          </div>
        )}
      </div>
      <div
        className={clsx(
          "rounded-3xl w-[78px] h-[26px] flex items-center justify-center text-xs",
          statusColor[pay.status]
        )}
      >
        {pay.status}
      </div>
    </div>
  );
};

export default PayCard;
