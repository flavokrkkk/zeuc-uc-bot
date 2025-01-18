import { IPack } from "@/entities/packs/types/types";
import { FC } from "react";

interface IPacksCard {
  pack: IPack;
  handleSelectPack: (event: React.MouseEvent<HTMLButtonElement>) => void;
}
const PacksCard: FC<IPacksCard> = ({ pack, handleSelectPack }) => {
  return (
    <button
      key={pack.id}
      value={pack.id}
      className="h-14 cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
      onClick={handleSelectPack}
    >
      {`${pack.value} (x${pack.multiplicationUc})`}
    </button>
  );
};

export default PacksCard;
