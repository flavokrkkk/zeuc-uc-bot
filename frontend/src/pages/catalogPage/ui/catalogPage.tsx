import { userSelectors } from "@/entities/user/models/store/userSlice";
import { usePacks } from "@/features/packs/hooks/usePacks";
import PacksList from "@/features/packs/ui/packsList";
import { useAppSelector } from "@/shared/hooks/useAppSelector";
import {
  Button,
  ButtonColors,
  ButtonRoundSizes,
  ButtonSizes,
} from "@/shared/ui/button/button";
import clsx from "clsx";

const CatalogPage = () => {
  const {
    isSelected,
    packs,
    totalPrice,
    totalPacks,
    handleSelectPack,
    handleUnSelectPack,
    handleSelectPacks,
  } = usePacks();

  const currentUser = useAppSelector(userSelectors.currentUser);
  const userInfo = useAppSelector(userSelectors.userInfo);

  return (
    <section
      className={clsx(
        "w-full  relative space-y-2 flex flex-col justify-between pt-2",
        isSelected && "pb-16"
      )}
    >
      <section className="space-y-5">
        <div className="text-white flex justify-between items-center">
          <h1>Привет 👋, {currentUser?.username}</h1>
          <span>
            <img
              src={userInfo?.photo_url}
              width={36}
              height={36}
              className="rounded-full"
            />
          </span>
        </div>
        <PacksList
          packs={packs}
          handleSelectPack={handleSelectPack}
          handleUnSelectPack={handleUnSelectPack}
        />
      </section>

      {isSelected && (
        <div className="fixed bottom-28 left-0 right-0 px-4 flex justify-center">
          <Button
            className="h-10 px-4 cursor-pointer w-full  bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
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
