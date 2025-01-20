import { usePacks } from "@/features/packs/hooks/usePacks";
import PacksList from "@/features/packs/ui/packsList";
import {
  Button,
  ButtonColors,
  ButtonRoundSizes,
  ButtonSizes,
} from "@/shared/ui/button/button";
import { IconTypes } from "@/shared/ui/icon/libs/libs";
import { Icon } from "@/shared/ui/icon/ui/icon";

const CatalogPage = () => {
  const {
    isSelected,
    packs,
    totalPrice,
    totalPacks,
    handleSelectPack,
    handleSelectPacks,
  } = usePacks();
  console.log(packs);
  return (
    <section className="w-full space-y-2 h-[90vh] flex flex-col justify-between pt-2">
      <section className="space-y-5">
        <div className="text-white flex justify-between items-center">
          <h1>Привет flavorkkk</h1>
          <span>
            <Icon type={IconTypes.AVATARKA_OUTLINED} />
          </span>
        </div>
        <PacksList packs={packs} handleSelectPack={handleSelectPack} />
      </section>

      {isSelected && (
        <div className="w-full space-x-1 flex justify-center">
          <Button
            className="h-10 w-full cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
            bgColor={ButtonColors.GREEN}
            rounded={ButtonRoundSizes.ROUNDED_XL}
            size={ButtonSizes.MEDIUM}
            onClick={handleSelectPacks}
          >
            {`Купить ${totalPacks} UC за ${totalPrice} рублей`}
          </Button>
        </div>
      )}
    </section>
  );
};

export default CatalogPage;
