import { usePacks } from "@/features/packs/hooks/usePacks";
import PacksList from "@/features/packs/ui/packsList";
import { ERouteNames } from "@/shared/libs/utils/pathVariables";
import { Link } from "react-router-dom";

const CatalogPage = () => {
  const {
    isSelected,
    packs,
    totalPrice,
    handleSelectPack,
    handleSelectPacks,
    handleUnSelectPack,
    handleResetTotalPacks,
  } = usePacks();
  return (
    <section className="w-full space-y-2">
      <Link
        to={ERouteNames.SCORES_PAGE}
        className="h-10  w-full  cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
      >
        Получить призы
      </Link>
      <PacksList
        packs={packs}
        handleSelectPack={handleSelectPack}
        setUnSelectPacks={handleUnSelectPack}
      />
      {isSelected && (
        <div className="w-full space-x-1 flex justify-center">
          <button
            className="h-10  w-full  cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
            onClick={handleSelectPacks}
          >
            Перейти к оплате {totalPrice}
          </button>
          <button
            className="h-10  w-full  cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
            onClick={handleResetTotalPacks}
          >
            Очистить выбор
          </button>
        </div>
      )}
    </section>
  );
};

export default CatalogPage;
