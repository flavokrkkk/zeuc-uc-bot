import { IUserDiscount } from "@/entities/user/types/types";
import { Check } from "lucide-react";
import { FC } from "react";

interface IDiscountCard {
  discount: IUserDiscount;
  totalPrice: number;
  discountId: number | null;
  handleUseDiscountId: (discountId: string) => void;
}

const DiscountCard: FC<IDiscountCard> = ({
  discount,
  discountId,
  totalPrice,
  handleUseDiscountId,
}) => {
  const handleIsCheck = (event: React.MouseEvent<HTMLInputElement>) => {
    if (!(discount.discount?.min_payment_value > totalPrice) || discountId) {
      const discountId = event.currentTarget.value;
      handleUseDiscountId(discountId);
    }
  };

  return (
    <div key={discount.discount.discount_id} className="flex space-x-4">
      <div className="flex space-x-3 items-center">
        <span>
          {discount.discount.value}₽ скидка на покупку от{" "}
          {discount.discount?.min_payment_value}₽
        </span>
      </div>
      <label className="flex items-center cursor-pointer">
        <input
          value={String(discount.discount.discount_id)}
          checked={discountId === discount.discount.discount_id}
          type="checkbox"
          className="hidden peer"
          onClick={handleIsCheck}
        />
        <div className="w-5 h-5 bg-gradient-to-r from-green-400 to-blue-500 rounded-md flex items-center justify-center transition-opacity duration-200 peer-checked:opacity-100 opacity-50">
          {discountId === discount.discount.discount_id && (
            <Check className="w-4 h-4 text-white transition-opacity duration-200 peer-checked:opacity-0" />
          )}
        </div>
      </label>
      {/* <Button
          value={String(discount.discount.discount_id)}
          isDisabled={
            discount.discount?.min_payment_value > totalPrice ||
            Boolean(discountId)
          }
          onClick={handleUseDiscountId}
        >
          Использовать
        </Button> */}
    </div>
  );
};

export default DiscountCard;
