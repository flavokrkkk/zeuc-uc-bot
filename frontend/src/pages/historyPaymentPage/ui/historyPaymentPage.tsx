import { userSelectors } from "@/entities/user/models/store/userSlice";
import { useHistoryPayment } from "@/features/payment/hooks/useHistoryPayment";
import HistoryPayment from "@/features/payment/ui/historyPayment";
import { useAppSelector } from "@/shared/hooks/useAppSelector";

const HistoryPaymentPage = () => {
  const currentUser = useAppSelector(userSelectors.currentUser);
  const userInfo = useAppSelector(userSelectors.userInfo);
  useHistoryPayment();
  return (
    <section className="w-full text-white space-y-2 flex flex-col justify-between pt-2">
      <section className="space-y-5">
        <div className="text-white flex justify-between items-center">
          <h1>Привет {currentUser?.username}</h1>
          <span>
            <span>
              <img
                src={userInfo?.photo_url}
                width={36}
                height={36}
                className="rounded-full"
              />
            </span>
          </span>
        </div>
        <HistoryPayment />
      </section>
    </section>
  );
};

export default HistoryPaymentPage;
