import { IPack } from "@/entities/uc/types/types";
import { FC } from "react";

interface IPacksList {
  packs: Array<IPack>;
  handleSelectPack: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

const PacksList: FC<IPacksList> = ({ packs, handleSelectPack }) => {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3 p-1">
      {packs.map((card) => (
        <button
          key={card.id}
          value={card.id}
          className="h-14 cursor-pointer bg-gray-200 border border-gray-300 flex items-center justify-center rounded-md"
          onClick={handleSelectPack}
        >
          {`${card.value} (x${card.multiplicationUc})`}
        </button>
      ))}
    </div>
  );
};

export default PacksList;
