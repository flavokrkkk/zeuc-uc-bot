import { ChevronDown, ChevronRight } from "lucide-react";
import { useState } from "react";

const TicketsContent = () => {
  const [isCheckHistory, setIsCheckHistory] = useState(false);

  const toggleIsHistory = () => setIsCheckHistory((prev) => !prev);

  return (
    <div className="bg-dark-200  rounded-xl p-4 px-10 space-y-5">
      <span className="text-yellow-300 text-[32px]">356 бонусов</span>
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
