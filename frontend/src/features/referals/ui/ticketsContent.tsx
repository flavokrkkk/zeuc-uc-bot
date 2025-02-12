import { userSelectors } from "@/entities/user/models/store/userSlice";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { IconTypes } from "@/shared/ui/icon/libs/libs";
import { Icon } from "@/shared/ui/icon/ui/icon";
import { ChevronDown, ChevronRight } from "lucide-react";
import { useState } from "react";

const TicketsContent = () => {
  const currentUser = useAppSelector(userSelectors.currentUser);
  const userBonusesHistory = useAppSelector(userSelectors.userBonusesHistory);
  const [isCheckHistory, setIsCheckHistory] = useState(false);
  const toggleIsHistory = () => setIsCheckHistory((prev) => !prev);

  return (
    <div className="bg-dark-200 rounded-2xl p-4 pb-8 py-7  px-10 space-y-5">
      <span className="text-yellow-300 text-[32px]">
        {currentUser?.bonuses} бонусов
      </span>
      <hr className="border-gray-600" />
      <div
        onClick={toggleIsHistory}
        className="text-white cursor-pointer flex items-center justify-between"
      >
        <span>Посмотреть историю начислений</span>
        <span>
          {isCheckHistory ? (
            <ChevronDown className="cursor-pointer" />
          ) : (
            <ChevronRight className="cursor-pointer" />
          )}
        </span>
      </div>
      {isCheckHistory && (
        <div className="text-gray-600 space-y-2">
          {userBonusesHistory.map((bonuses) => (
            <div
              key={bonuses.id}
              className="flex justify-between border-b border-gray-600 pb-2"
            >
              <section className="flex flex-col">
                <div className="text-sm flex space-x-2">
                  <span className="font-bold">Количество -</span>
                  <span className="flex space-x-1 items-center">
                    <span>{bonuses.amount}</span>
                    <Icon type={IconTypes.POINT_OUTLINED} />
                  </span>
                </div>
                <div className="text-sm">
                  <span className="font-bold">Дата покупки - </span>{" "}
                  <span className="underline">{bonuses.created_at}</span>
                </div>
                <div className="text-sm">
                  <span className="font-bold">Статус</span> -{" "}
                  <span className="text-green-100">{bonuses.status}</span>
                </div>
              </section>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TicketsContent;
