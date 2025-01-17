import { ucSelectors } from "@/entities/uc/model/store/ucSlice";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import { Link } from "react-router-dom";

const PaymentPage = () => {
  const totalUc = useAppSelector(ucSelectors.totalUc);
  const totalPrice = useAppSelector(ucSelectors.totalPrice);
  return (
    <div className="space-y-5 text-white">
      <Link to={ERouteNames.CATALOG_PAGE}>Назад</Link>
      <h1 className="text-2xl mb-4">Ваш заказ:</h1>
      <section className="flex justify-between">
        <span>{`${totalUc} UC`}</span>
        <span>{`${totalPrice} ₽`}</span>
      </section>
      <hr />
      <section className="flex w-full justify-between items-center">
        <div>
          <h2>Ваш ID: 1131</h2>
          <h2>Ваш ник: 1131</h2>
        </div>
        <div>
          <button className="h-10 px-4  w-full  cursor-pointer bg-gray-200 border text-gray-400 border-gray-300 flex items-center justify-center rounded-md">
            Изменить ID
          </button>
        </div>
      </section>
      <h1 className="text-2xl mb-4">Выберите способ оплаты: </h1>
      <section className="flex space-x-2">
        <div className="border p-5 w-full rounded-md">
          {`Оплатить спб ${totalPrice}₽`}
        </div>
        <div className="border p-5 w-full rounded-md">
          {`Оплатить картой ${totalPrice}₽`}
        </div>
      </section>
    </div>
  );
};

export default PaymentPage;
