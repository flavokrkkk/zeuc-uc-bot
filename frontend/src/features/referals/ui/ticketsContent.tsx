import { userSelectors } from "@/entities/user/models/store/userSlice";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { ChevronDown, ChevronRight } from "lucide-react";
import { useState } from "react";

const TicketsContent = () => {
  const currentUser = useAppSelector(userSelectors.currentUser);
  const [isCheckHistory, setIsCheckHistory] = useState(false);

  const toggleIsHistory = () => setIsCheckHistory((prev) => !prev);

  return (
    <div className="bg-dark-200 rounded-2xl p-4 pb-8 py-7  px-10 space-y-5">
      <span className="text-yellow-300 text-[32px]">
        {currentUser?.bonuses} бонусов
      </span>
      <hr className="border-gray-600" />
      <div className="text-white flex items-center justify-between">
        <span>Посмотреть историю начислений</span>
        <span onClick={toggleIsHistory}>
          {isCheckHistory ? (
            <ChevronDown className="cursor-pointer" />
          ) : (
            <ChevronRight className="cursor-pointer" />
          )}
        </span>
      </div>
      {isCheckHistory && (
        <div className="text-gray-600">
          <div className="flex justify-between">
            <span>25 бонусов</span>
            <span>23.12.2024</span>
          </div>
          <div className="flex justify-between">
            <span>25 бонусов</span>
            <span>23.12.2024</span>
          </div>
          <div className="flex justify-between">
            <span>25 бонусов</span>
            <span>23.12.2024</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default TicketsContent;
