import { IPack } from "@/entities/packs/types/types";
import { IconTypes } from "@/shared/ui/icon/libs/libs";
import { Icon } from "@/shared/ui/icon/ui/icon";
import { FC } from "react";

interface IPacksBadge {
  pack: IPack;
  handleSelectPack: (event: React.MouseEvent<HTMLButtonElement>) => void;
  handleUnSelectPack: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

const PacksBadge: FC<IPacksBadge> = ({
  pack,
  handleSelectPack,
  handleUnSelectPack,
}) => {
  return (
    <div
      key={pack.id}
      className="bg-dark-200 h-[48px] p-1 px-5 rounded-lg flex items-center justify-between"
    >
      <div className="flex space-x-2 items-center">
        <span>{pack.uc_amount}</span>
        <span>
          <Icon type={IconTypes.UC_OUTLINED} />
        </span>
      </div>
      <div className=" bg-gray-dark-100 w-[94px] h-[32px] flex items-center justify-between px-2 rounded-lg">
        <button
          disabled={pack.multiplication_uc === 1}
          value={pack.id}
          className="rounded-lg flex items-center justify-center cursor-pointer h-full w-full"
          onClick={handleUnSelectPack}
        >
          <Icon type={IconTypes.MINUS_OUTLINED} />
        </button>

        <button className="rounded-lg h-full w-full">
          {pack.multiplication_uc}
        </button>
        <button
          value={pack.id}
          className="rounded-lg cursor-pointer h-full w-full flex items-center justify-center"
          onClick={handleSelectPack}
        >
          <Icon type={IconTypes.PLUS_OUTLINED} />
        </button>
      </div>
      <div className="space-x-1 text-white">
        <span>{pack.price_per_uc.price} рублей</span>
      </div>
    </div>
  );
};
export default PacksBadge;
