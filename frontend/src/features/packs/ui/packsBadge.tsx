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
      className="bg-dark-200 p-2 px-5 rounded-lg flex items-center justify-between"
    >
      <div className="flex space-x-2 items-center">
        <span>{pack.ucinitial}</span>
        <span>
          <Icon type={IconTypes.UC_OUTLINED} />
        </span>
      </div>
      <div className="space-x-1">
        <button
          value={pack.id}
          className="bg-gray-700 p-3 px-5 rounded-lg"
          onClick={handleSelectPack}
        >
          +
        </button>
        <button className=" bg-gray-700 p-3 px-5 rounded-lg">
          {pack.multiplication_uc}
        </button>
        <button
          disabled={pack.multiplication_uc === 1}
          value={pack.id}
          className=" bg-gray-700 p-3 px-5 rounded-lg"
          onClick={handleUnSelectPack}
        >
          -
        </button>
      </div>
      <div className="space-x-1 text-white">
        <span>{pack.price_per_uc.price} рублей</span>
      </div>
    </div>
  );
};
export default PacksBadge;
