import { IPack } from "@/entities/packs/types/types";
import { FC } from "react";

interface IPaymentInfo {
  totalPacks: number;
  totalPrice: number;
  selectedPacks: Array<IPack>;
}

const PaymentInfo: FC<IPaymentInfo> = ({
  totalPrice,
  totalPacks,
  selectedPacks,
}) => {
  return (
    <section>
      <section className="flex  flex-col">
        <span>{`Total UC ${totalPacks} UC`}</span>
        <span>{`Total RUB ${totalPrice} ₽`}</span>
        {selectedPacks.map((el) => (
          <span key={el.id}>{`Packs ${el.value} x${el.multiplicationUc}`}</span>
        ))}
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
    </section>
  );
};

export default PaymentInfo;
