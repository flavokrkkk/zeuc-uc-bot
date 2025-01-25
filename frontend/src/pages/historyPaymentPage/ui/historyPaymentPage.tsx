import { userSelectors } from "@/entities/user/models/store/userSlice";
import { useHistoryPayment } from "@/features/payment/hooks/useHistoryPayment";
import HistoryPayment from "@/features/payment/ui/historyPayment";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { IconTypes } from "@/shared/ui/icon/libs/libs";
import { Icon } from "@/shared/ui/icon/ui/icon";

const HistoryPaymentPage = () => {
  const currentUser = useAppSelector(userSelectors.currentUser);
  useHistoryPayment();
  return (
    <section className="w-full text-white space-y-2 flex flex-col justify-between pt-2">
      <section className="space-y-5">
        <div className="text-white flex justify-between items-center">
          <h1>Привет {currentUser?.username}</h1>
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
