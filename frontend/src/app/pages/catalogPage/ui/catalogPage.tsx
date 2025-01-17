import { ucSelectors } from "@/entities/uc/model/store/ucSlice";
import { useActions } from "@/shared/hooks/useActions";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import { Link } from "react-router-dom";

const CatalogPage = () => {
  const isSelected = useAppSelector(ucSelectors.isSelected);
  const ucCards = useAppSelector(ucSelectors.getUcSelects);
  const totalPrice = useAppSelector(ucSelectors.totalPrice);

  const { setSelectUc } = useActions();

  const handleSelectUc = (event: React.MouseEvent<HTMLButtonElement>) => {
    if (!event.currentTarget.value) throw new Error("Invalidate id uc!");
    setSelectUc(Number(event.currentTarget.value));
  };

  return (
    <section className="w-full space-y-2">
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3 p-1">
        {ucCards.map((card) => (
          <button
            key={card.id}
            value={card.id}
            className="h-14 cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
            onClick={handleSelectUc}
          >
            {`${card.value} (x${card.multiplicationUc})`}
          </button>
        ))}
      </div>
      {isSelected && (
        <div className="w-full flex justify-center">
          <Link
            to={ERouteNames.PAYMENT_PAGE}
            className="h-10  w-full  cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
          >
            Перейти к оплате {totalPrice}
          </Link>
        </div>
      )}
    </section>
  );
};

export default CatalogPage;
