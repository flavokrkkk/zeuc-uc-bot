import { IPack } from "@/entities/packs/types/types";
import PacksBadge from "@/features/packs/ui/packsBadge";
import { FC, useCallback } from "react";
import { useActions } from "@/shared/hooks/useActions";
import { useNavigate } from "react-router-dom";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { userSelectors } from "@/entities/user/models/store/userSlice";
import DiscountCard from "./discountCard";

interface IPaymentInfo {
  discountId: number | null;
  totalPacks: number;
  totalPrice: number;
  selectedPacks: Array<IPack>;
  handleUseDiscountId: (discountId: string) => void;
  handleSelectPack: (event: React.MouseEvent<HTMLButtonElement>) => void;
  handleUnSelectPack: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

const PaymentInfo: FC<IPaymentInfo> = ({
  totalPrice,
  totalPacks,
  discountId,
  selectedPacks,
  handleUseDiscountId,
  handleSelectPack,
  handleUnSelectPack,
}) => {
  const { setUnSelectPacks } = useActions();
  const userDiscount = useAppSelector(userSelectors.userDiscount);
  const navigate = useNavigate();

  const handleDeletePack = useCallback(
    (event: React.MouseEvent<HTMLButtonElement>) => {
      if (!event.currentTarget.value) throw new Error("Not a valid value!");
      if (selectedPacks.length === 1) {
        setUnSelectPacks({ id: event.currentTarget.value, type: "total" });
        navigate(ERouteNames.CATALOG_PAGE, { replace: true });
        return;
      }
      setUnSelectPacks({ id: event.currentTarget.value, type: "total" });
    },
    [selectedPacks.length]
  );

  return (
    <section className="space-y-4">
      <section className="flex  flex-col">
        <div className="space-y-2">
          {selectedPacks.map((pack) => (
            <PacksBadge
              key={pack.id}
              pack={pack}
              handleSelectPack={handleSelectPack}
              handleUnSelectPack={handleUnSelectPack}
              handleDeletePack={handleDeletePack}
            />
          ))}
        </div>
      </section>
      <section className="flex w-full space-y-3 flex-col justify-end items-end">
        <div className="space-x-2">
          <span>Итого:</span>
          <span className="text-2xl">{`${totalPacks} UC | ${totalPrice} ₽`}</span>
        </div>
        {userDiscount.map((discount, index) => (
          <DiscountCard
            key={index}
            discount={discount}
            discountId={discountId}
            totalPrice={totalPrice}
            handleUseDiscountId={handleUseDiscountId}
          />
        ))}
      </section>
      <hr />
    </section>
  );
};

export default PaymentInfo;
