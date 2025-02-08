import { userSelectors } from "@/entities/user/models/store/userSlice";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
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
        <div className="text-gray-600">
          {userBonusesHistory.map((bonuses) => (
            <div key={bonuses.id} className="flex justify-between">
              <span>{bonuses.amount} бонусов</span>
              <span>{bonuses.amount}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TicketsContent;
