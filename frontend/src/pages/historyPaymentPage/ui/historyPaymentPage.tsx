import HistoryPayment from "@/features/payment/ui/historyPayment";
import { IconTypes } from "@/shared/ui/icon/libs/libs";
import { Icon } from "@/shared/ui/icon/ui/icon";

const HistoryPaymentPage = () => {
  return (
    <section className="w-full text-white space-y-2 flex flex-col justify-between pt-2">
      <section className="space-y-5">
        <div className="text-white flex justify-between items-center">
          <h1>Привет flavorkkk</h1>
          <span>
            <Icon type={IconTypes.AVATARKA_OUTLINED} />
          </span>
        </div>
        <HistoryPayment />
      </section>
    </section>
  );
};

export default HistoryPaymentPage;
