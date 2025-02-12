import PayCard from "./payCard";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { userSelectors } from "@/entities/user/models/store/userSlice";
import {
  Button,
  ButtonColors,
  ButtonRoundSizes,
} from "@/shared/ui/button/button";
import { Link } from "react-router-dom";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import { Icon } from "@/shared/ui/icon/ui/icon";
import { IconTypes } from "@/shared/ui/icon/libs/libs";

const HistoryPayment = () => {
  const userPaymentHistory = useAppSelector(userSelectors.userPaymentHistory);
  return (
    <div className="space-y-4 h-full ">
      <h1 className="text-2xl">История заказов</h1>
      {!userPaymentHistory.length ? (
        <div className="space-y-2">
          {userPaymentHistory.map((pay, index) => (
            <PayCard key={index} pay={pay} />
          ))}
        </div>
      ) : (
        <div className="absolute inset-0 flex flex-col items-center justify-center space-y-4">
          <div className="text-center">
            <div className="flex justify-center items-center space-x-2">
              <h2 className="text-xl font-semibold">У вас пока нет заказов</h2>
              <Icon type={IconTypes.UC_OUTLINED} />
            </div>

            <p className="text-gray-600">
              Не упустите возможность сделать свой первый заказ!
            </p>
          </div>
          <div className="w-full px-14">
            <Link to={ERouteNames.CATALOG_PAGE}>
              <Button
                className="w-full py-2"
                bgColor={ButtonColors.GREEN}
                rounded={ButtonRoundSizes.ROUNDED_XL}
              >
                Выбрать
              </Button>
            </Link>
          </div>
        </div>
      )}
    </div>
  );
};

export default HistoryPayment;
