import { FC } from "react";

export interface IPaymentMethod {
  totalPrice: number;
}

const PaymentMethod: FC<IPaymentMethod> = ({ totalPrice }) => {
  return (
    <section className="flex space-x-2">
      <div className="border p-5 w-full rounded-md">
        {`Оплатить спб ${totalPrice}₽`}
      </div>
      <div className="border p-5 w-full rounded-md">
        {`Оплатить картой ${totalPrice}₽`}
      </div>
    </section>
  );
};

export default PaymentMethod;
