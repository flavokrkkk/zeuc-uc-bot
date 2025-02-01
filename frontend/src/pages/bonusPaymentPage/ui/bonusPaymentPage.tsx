import { usePoints } from "@/features/user/hooks/usePoints";
import {
  Button,
  ButtonColors,
  ButtonRoundSizes,
} from "@/shared/ui/button/button";
import { IconTypes } from "@/shared/ui/icon/libs/libs";
import { Icon } from "@/shared/ui/icon/ui/icon";
import { Input } from "@/shared/ui/input/input";
import { CreditCard } from "lucide-react";

const BonusPaymentPage = () => {
  const { handleGetPayLink, handleChangePoints, points, isPending } =
    usePoints();
  return (
    <div className=" text-white flex items-center justify-center p-4">
      <div className="max-w-md w-full rounded-xl shadow-2xl p-8">
        <h1 className="text-3xl font-medium text-center mb-8">
          Покупка бонусов
        </h1>

        <div className="mb-6">
          <Input
            type="number"
            placeholder="Введите количество бонусов..."
            value={points}
            onChange={handleChangePoints}
          />
        </div>

        <div className="flex items-center justify-between bg-dark-200 p-4 rounded-lg mb-8">
          <span className="text-lg font-medium">К оплате</span>
          <span className="text-2xl font-medium flex items-center">
            {Number(points) * 5} ₽
          </span>
        </div>

        <div className="flex flex-col w-full space-y-4">
          <Button
            value="sbp"
            className="h-14 w-full cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
            bgColor={ButtonColors.GREEN}
            isDisabled={isPending}
            rounded={ButtonRoundSizes.ROUNDED_XL}
            onClick={handleGetPayLink}
          >
            <span className="flex space-x-2 items-center">
              <Icon type={IconTypes.SBP_OUTLINED} />
              <span>Оплатить через СБП</span>
            </span>
          </Button>
          <Button
            value="card"
            isDisabled={isPending}
            className="h-14 w-full cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
            bgColor={ButtonColors.GREEN}
            rounded={ButtonRoundSizes.ROUNDED_XL}
            onClick={handleGetPayLink}
          >
            <span className="flex space-x-2 items-center">
              <CreditCard />
              <span>Оплатить картой</span>
            </span>
          </Button>
        </div>
      </div>
    </div>
  );
};

export default BonusPaymentPage;
