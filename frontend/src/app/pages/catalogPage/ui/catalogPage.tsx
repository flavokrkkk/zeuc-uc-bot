import { usePacks } from "@/features/packs/hooks/usePacks";
import PacksList from "@/features/packs/ui/packsList";

const CatalogPage = () => {
  const { isSelected, packs, totalPrice, handleSelectPack, handleSelectPacks } =
    usePacks();
  return (
    <section className="w-full space-y-2">
      <PacksList packs={packs} handleSelectPack={handleSelectPack} />
      {isSelected && (
        <div className="w-full flex justify-center">
          <button
            className="h-10  w-full  cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
            onClick={handleSelectPacks}
          >
            Перейти к оплате {totalPrice}
          </button>
        </div>
      )}
    </section>
  );
};

export default CatalogPage;
